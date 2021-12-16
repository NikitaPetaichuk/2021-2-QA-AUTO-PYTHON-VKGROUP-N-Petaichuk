import json
import logging
from urllib.parse import urljoin

import requests

from static.links import Links
from static.tests_config import TestsConfig


class UnexpectedResponseStatusCodeException(Exception):
    pass


class AppAPIClient:

    def __init__(self, base_url, username, email, password):
        self.base_url = base_url
        self.username = username
        self.email = email
        self.password = password
        self.logger = logging.getLogger('tests')
        self.session = requests.Session()

    def _log_before_request(self, url, headers, data, expected_status):
        self.logger.info(
            f'PERFORMING REQUEST:\n'
            f'URL: {url}\n'
            f'HEADERS: {headers}\n'
            f'DATA: {data}\n'
            f'EXPECTED STATUS: {expected_status}\n'
        )

    def _log_after_request(self, response):
        log_header = f'Got response:\n' \
                     f'RESPONSE STATUS: {response.status_code}\n' \
                     f'RESPONSE HEADERS: {response.headers}'
        if len(response.text) > TestsConfig.MAX_RESPONSE_LENGTH:
            self.logger.info(
                f'{log_header}\n'
                f'RESPONSE CONTENT: COLLAPSED due to response size > {TestsConfig.MAX_RESPONSE_LENGTH}:\n'
                f'{response.text[:TestsConfig.MAX_RESPONSE_LENGTH]}\n'
            )
        else:
            self.logger.info(
                f'{log_header}\n'
                f'RESPONSE CONTENT: {response.text}\n'
            )

    def _make_request(self, method, url, headers=None, data=None, expected_status=200, jsonify=False):
        self._log_before_request(url, headers, data, expected_status)
        response = self.session.request(method, url, headers=headers, data=data, allow_redirects=True)
        self._log_after_request(response)

        if response.status_code != expected_status:
            raise UnexpectedResponseStatusCodeException(
                f'Got {response.status_code} response for URL "{url}" (expected {expected_status})'
            )
        if jsonify:
            return response.json()
        return response

    def post_register_client(self):
        self.logger.info("Register client in app")

        request_url = urljoin(self.base_url, "reg")
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "confirm": self.password,
            "term": "y",
            "submit": "Register"
        }
        self._make_request("POST", request_url, headers=headers, data=data)

    def get_user_blocked(self, username, expected_status=200):
        self.logger.info(f"Blocking user with name '{username}'")

        request_url = urljoin(self.base_url, f"{Links.APP_API_BLOCK_USER_PART}{username}")
        self._make_request("GET", request_url, expected_status=expected_status)

    def get_user_unblocked(self, username, expected_status=200):
        self.logger.info(f"Unblocking user with name '{username}'")

        request_url = urljoin(self.base_url, f"{Links.APP_API_UNBLOCK_USER_PART}{username}")
        self._make_request("GET", request_url, expected_status=expected_status)

    def post_add_user(self, user_data, expected_status=200):
        self.logger.info(f"Adding new user with params '{user_data}'")

        request_url = urljoin(self.base_url, Links.APP_API_ADD_USER_PART)
        headers = {
            'Content-Type': 'application/json'
        }
        data = json.dumps(user_data)
        self._make_request("POST", request_url, headers=headers, data=data, expected_status=expected_status)

    def get_user_delete(self, username, expected_status=200):
        self.logger.info(f"Deleting user with name '{username}'")

        request_url = urljoin(self.base_url, f"{Links.APP_API_DELETE_USER_PART}{username}")
        self._make_request("GET", request_url, expected_status=expected_status)
