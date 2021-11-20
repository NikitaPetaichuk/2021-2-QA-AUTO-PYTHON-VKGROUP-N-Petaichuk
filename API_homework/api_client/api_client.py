import logging

import requests
from urllib.parse import urljoin

from static.tests_config import TestsConfig
from utils.json_generator import RequestsDataGenerator


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
            'Referer': self.base_url
        }

    @property
    def post_act_with_segments_headers(self):
        return {
            'Content-Type': 'application/json',
            'X-CSRFToken': self.csrf_token
        }

    @property
    def post_send_picture_headers(self):
        return {
            'X-CSRFToken': self.csrf_token
        }

    @property
    def post_created_campaigns_headers(self):
        return {
            'Content-Type': 'application/json',
            'X-CSRFToken': self.csrf_token
        }

    @property
    def post_delete_campaign_headers(self):
        return {
            'Content-Type': 'application/json',
            'X-CSRFToken': self.csrf_token
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

    def _make_request(self, method, url, headers=None, data=None, expected_status=200, jsonify=False):
        self._log_before_request(url, headers, data, expected_status)
        response = self.session.request(method, url, headers=headers, data=data, allow_redirects=True)
        self._log_after_request(response)

        if response.status_code != expected_status:
            raise UnexpectedResponseStatusCodeException(
                f'Got {response.status_code} {response.request} for URL "{url}"'
            )
        if jsonify:
            return response.json()
        return response

    def _get_csrf_token(self):
        request_url = urljoin(self.base_url, 'csrf/')
        set_cookie_headers = self._make_request("GET", request_url).headers['set-cookie']
        token_part = set_cookie_headers.split(';')[0]
        self.csrf_token = token_part.split('=')[1]

    def post_login(self):
        self.logger.info("Logging into MyTarget")

        login_url = TestsConfig.LOGIN_URL
        headers = self.post_login_headers
        data = RequestsDataGenerator.generate_data_for_login(self.email, self.password)
        self._make_request("POST", login_url, headers=headers, data=data)
        self._get_csrf_token()

    def post_create_segment(self, segment_name):
        self.logger.info(f"Creating the segment with the name '{segment_name}'")

        request_url = urljoin(self.base_url, "api/v2/remarketing/segments.json?fields=id,name")
        headers = self.post_act_with_segments_headers
        data = RequestsDataGenerator.generate_json_for_creating_segment(segment_name)
        return self._make_request("POST", request_url, headers=headers, data=data, jsonify=True)

    def get_segment(self, segment_id):
        self.logger.info(f"Getting the segment with ID {segment_id}")

        request_url = urljoin(self.base_url, f"api/v2/coverage/segment.json?id={segment_id}")
        response = self._make_request("GET", request_url, jsonify=True)
        return None if response["items"][0]["status"] == "not found" else response["items"][0]

    def post_delete_segment(self, segment_id):
        self.logger.info(f"Deleting the segment with ID {segment_id}")

        location_url = urljoin(self.base_url, "api/v1/remarketing/mass_action/delete.json")
        headers = self.post_act_with_segments_headers
        data = RequestsDataGenerator.generate_json_for_deleting_segment(segment_id)
        return self._make_request("POST", location_url, headers=headers, data=data, jsonify=True)

    def get_url_id(self, url):
        self.logger.info(f"Getting ID for the URL {url}")

        request_url = urljoin(self.base_url, f'api/v1/urls/?url={url}')
        response = self._make_request("GET", request_url, jsonify=True)
        return response["id"]

    def get_picture_id(self, picture_name, picture_path):
        self.logger.info(f"Getting ID for the picture with name {picture_name} and path {picture_path}")

        request_url = urljoin(self.base_url, 'api/v2/content/static.json')
        headers = self.post_send_picture_headers
        with open(picture_path, 'rb') as picture:
            files = RequestsDataGenerator.generate_files_for_sending_picture(picture_name, picture)
            response = self.session.post(request_url, headers=headers, files=files)
            return response.json()["id"]

    def post_create_traffic_banner_campaign(self, campaign_name, picture_path):
        self.logger.info(f"Creating the traffic banner campaign with the name '{campaign_name}'")

        url_id = self.get_url_id(TestsConfig.TARGET_URL)
        picture_id = self.get_picture_id(TestsConfig.PICTURE_NAME, picture_path)

        location_url = urljoin(self.base_url, 'api/v2/campaigns.json')
        headers = self.post_created_campaigns_headers
        data = RequestsDataGenerator.generate_json_for_creating_campaign(campaign_name, url_id, picture_id)
        return self._make_request("POST", location_url, headers=headers, data=data, jsonify=True)

    def get_campaigns_count(self):
        self.logger.info("Getting the campaigns count")

        request_url = urljoin(self.base_url, "api/v2/campaigns.json")
        response = self._make_request("GET", request_url, jsonify=True)
        return response['count']

    def get_campaigns(self):
        self.logger.info(f"Getting the campaigns list")

        campaigns_count = self.get_campaigns_count()
        request_url = urljoin(self.base_url, f"api/v2/campaigns.json?fields=id&limit={campaigns_count}")
        response = self._make_request("GET", request_url, jsonify=True)
        return response["items"]

    def post_delete_campaign(self, campaign_id):
        self.logger.info(f"Deleting the campaign with the name '{campaign_id}'")

        location_url = urljoin(self.base_url, 'api/v2/campaigns/mass_action.json')
        headers = self.post_delete_campaign_headers
        data = RequestsDataGenerator.generate_json_for_deleting_campaign(campaign_id)
        return self._make_request("POST", location_url, headers=headers, data=data, expected_status=204)
