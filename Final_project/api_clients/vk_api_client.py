import logging
from urllib.parse import urljoin

import requests


class VkAPIClient:

    def __init__(self, host, port):
        self.base_url = f'http://{host}:{port}'
        self.logger = logging.getLogger('tests')
        self.session = requests.Session()

    def _log_request(self, response):
        request = response.request
        self.logger.info(
            f'PERFORMED REQUEST:\n'
            f'METHOD: {request.method}\n'
            f'URL: {request.url}\n'
            f'HEADERS: {request.headers}\n'
            f'DATA: {request.body}\n\n'
            f'GOT RESPONSE:\n'
            f'RESPONSE STATUS: {response.status_code}\n'
            f'RESPONSE HEADERS: {response.headers}\n'
            f'RESPONSE CONTENT: {response.text}'
        )

    def create_vk_id(self, username, user_id):
        self.logger.info(f"Creating new VK ID '{user_id}' for '{username}'")

        request_url = urljoin(self.base_url, '/vk_id/create_id')
        request_data = {
            "username": username,
            "id": user_id
        }
        response = self.session.request("POST", request_url, json=request_data)
        self._log_request(response)

    def update_vk_id(self, username, new_id):
        self.logger.info(f"Updating VK ID for '{username}': new ID is '{new_id}'")

        request_url = urljoin(self.base_url, '/vk_id/update_id')
        request_data = {
            "username": username,
            "new_id": new_id
        }
        response = self.session.request("PUT", request_url, json=request_data)
        self._log_request(response)

    def delete_vk_id(self, username):
        self.logger.info(f"Deleting VK ID for '{username}'")

        request_url = urljoin(self.base_url, f'/vk_id/delete_id/{username}')
        response = self.session.request("DELETE", request_url)
        self._log_request(response)
