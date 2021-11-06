import json
import logging

import requests
from urllib.parse import urljoin

from static.tests_config import TestsConfig


class UnexpectedResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.logger = logging.getLogger('tests')
        self.session = requests.Session()
        self.csrf_token = None

    @property
    def post_login_headers(self):
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://target.my.com/'
        }

    @property
    def post_act_with_segments_headers(self):
        return {
            'Content-Type': 'application/json',
            'Referer': 'https://target.my.com/segments/segments_list/new/',
            'X-CSRFToken': self.csrf_token
        }

    @property
    def post_created_campaigns_headers(self):
        return {
            'Content-Type': 'application/json',
            'Referer': 'https://target.my.com/campaign/new',
            'X-CSRFToken': self.csrf_token
        }

    @property
    def post_delete_campaign_headers(self):
        return {
            'Content-Type': 'application/json',
            'Referer': 'https://target.my.com/dashboard',
            'X-CSRFToken': self.csrf_token
        }

    @staticmethod
    def _generate_get_headers(referer):
        return {
            'Referer': referer
        }

    def _log_before_request(self, url, headers, data, expected_status):
        self.logger.info(
            f'Performing request:\n'
            f'URL: {url}\n'
            f'HEADERS: {headers}\n'
            f'DATA: {data}\n'
            f'expected status: {expected_status}\n\n'
        )

    def _log_after_request(self, response):
        log_header = f'Got response:\n' \
                     f'RESPONSE STATUS: {response.status_code}'
        if len(response.text) > TestsConfig.MAX_RESPONSE_LENGTH:
            self.logger.info(
                f'{log_header}\n'
                f'RESPONSE CONTENT: COLLAPSED due to response size > {TestsConfig.MAX_RESPONSE_LENGTH}:\n'
                f'{response.text[:TestsConfig.MAX_RESPONSE_LENGTH]}\n\n'
            )
        else:
            self.logger.info(
                f'{log_header}\n'
                f'RESPONSE CONTENT: {response.text}\n\n'
            )

    def _make_request(self, method, url, headers=None, data=None, expected_status=200, jsonify=False, use_base=True):
        if use_base:
            url_to_request = urljoin(self.base_url, url)
        else:
            url_to_request = url

        self._log_before_request(url_to_request, headers, data, expected_status)
        response = self.session.request(
            method, url_to_request, headers=headers, data=data, allow_redirects=True
        )
        self._log_after_request(response)

        if response.status_code != expected_status:
            raise UnexpectedResponseStatusCodeException(
                f'Got {response.status_code} {response.request} for URL "{url_to_request}"'
            )
        if jsonify:
            json_response = response.json()
            return json_response
        return response

    def _get_csrf_token(self):
        location_url = 'csrf/'
        headers = self._generate_get_headers('https://target.my.com/dashboard')
        set_cookie_headers = self._make_request("GET", location_url, headers=headers).headers['set-cookie']
        token_part = set_cookie_headers.split(';')[0]
        self.csrf_token = token_part.split('=')[1]

    def post_login(self):
        self.logger.info("Logging into MyTarget.")

        login_url = TestsConfig.LOGIN_URL
        headers = self.post_login_headers
        data = {
            'email': self.email,
            'password': self.password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }
        self._make_request(
            "POST", login_url, headers=headers, data=data, use_base=False
        )
        self._get_csrf_token()

    def post_create_segment(self, segment_name):
        self.logger.info(f"Creating the segment with the name '{segment_name}'")

        location_url = "api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id," \
                       "relations__params,relations__params__score,relations__id,relations_count,id,name," \
                       "pass_condition,created,campaign_ids,users,flags"
        headers = self.post_act_with_segments_headers
        data = json.dumps({
            "logicType": "or",
            "name": segment_name,
            "pass_condition": 1,
            "relations": [
                {
                    "object_type": "remarketing_player",
                    "params": {
                        "type": "positive",
                        "left": 365,
                        "right": 0
                    }
                }
            ]
        })
        response = self._make_request("POST", location_url, headers=headers, data=data, jsonify=True)
        return response

    def get_segment(self, segment_id):
        self.logger.info(f"Getting the segment with id {segment_id}")

        location_url = f"api/v2/coverage/segment.json?id={segment_id}"
        headers = self._generate_get_headers('https://target.my.com/segments/segments_list')
        response = self._make_request("GET", location_url, headers=headers, jsonify=True)
        return response["items"][0]

    def post_delete_segment(self, segment_id):
        self.logger.info(f"Deleting the segment with id {segment_id}")

        location_url = "api/v1/remarketing/mass_action/delete.json"
        headers = self.post_act_with_segments_headers
        data = json.dumps([
            {"source_id": segment_id, "source_type": "segment"}
        ])
        response = self._make_request("POST", location_url, headers=headers, data=data, jsonify=True)
        return response

    def post_create_traffic_banner_campaign(self, campaign_name):
        self.logger.info(f"Creating the traffic banner campaign with the name '{campaign_name}'")

        location_url = 'api/v2/campaigns.json'
        headers = self.post_created_campaigns_headers
        data = json.dumps({
            "name": campaign_name,
            "objective": "traffic",
            "package_id": 961,
            "banners": [{
                "urls": {
                    "primary": {
                        "id": 1852176
                    }
                },
                "textblocks": {},
                "content": {
                    "image_240x400": {
                        "id": 2180798
                    }
                },
                "name": ""
            }]
        })
        response = self._make_request("POST", location_url, headers=headers, data=data, jsonify=True)
        return response

    def get_campaigns_count(self):
        self.logger.info("Getting campaigns count")

        location_url = f"api/v2/campaigns.json?_user_id__in={TestsConfig.MY_TARGET_USER_ID}"
        headers = self._generate_get_headers('https://target.my.com/dashboard')
        response = self._make_request("GET", location_url, headers=headers, jsonify=True)
        self.logger.info(f"Got count: {response['count']}")
        return response["count"]

    def get_last_added_campaign(self):
        self.logger.info("Getting the last added campaign")

        campaigns_count = self.get_campaigns_count()
        location_url = f"api/v2/campaigns.json?fields=id&offset={campaigns_count - 1}&" \
                       f"_user_id__in={TestsConfig.MY_TARGET_USER_ID}"
        headers = self._generate_get_headers('https://target.my.com/dashboard')
        response = self._make_request("GET", location_url, headers=headers, jsonify=True)
        return response["items"][0]

    def post_delete_campaign(self, campaign_id):
        self.logger.info(f"Deleting the campaign with the name '{campaign_id}'")

        location_url = 'api/v2/campaigns/mass_action.json'
        headers = self.post_delete_campaign_headers
        data = json.dumps([{
            "id": campaign_id,
            "status": "deleted"
        }])
        self._make_request("POST", location_url, headers=headers, data=data, expected_status=204)
