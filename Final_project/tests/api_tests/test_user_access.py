from urllib.parse import urljoin

import pytest
import requests

from static.links import Links
from tests.api_tests.base_api import BaseCaseAPI


class TestUserAccess(BaseCaseAPI):

    @pytest.fixture(scope='function', autouse=True)
    def setup_user_for_testing(self):
        user_data = self.user_builder.create_user_data()
        self.mysql_client.add_user(user_data)
        self.testing_user_data = user_data
        yield
        self.mysql_client.delete_user(user_data["email"])

    def check_user_access_status(self, user_email, access_status):
        user_entity = self.mysql_client.get_user("email", user_email)
        assert user_entity.access == access_status

    def test_block_user(self):
        self.check_request(self.api_client.get_user_blocked, self.testing_user_data["username"])

        self.check_user_access_status(self.testing_user_data["email"], 0)

    def test_block_blocked_user(self):
        self.mysql_client.set_user_access(self.testing_user_data["email"], 0)

        self.check_request(self.api_client.get_user_blocked, self.testing_user_data["username"], 304)

        self.check_user_access_status(self.testing_user_data["email"], 0)

    def test_block_non_existent_user(self, faker):
        non_existent_username = faker.pystr(max_chars=20, min_chars=0)

        self.check_request(self.api_client.get_user_blocked, non_existent_username, 404)

    def test_unblock_user(self):
        self.mysql_client.set_user_access(self.testing_user_data["email"], 0)

        self.check_request(self.api_client.get_user_unblocked, self.testing_user_data["username"])

        self.check_user_access_status(self.testing_user_data["email"], 1)

    def test_unblock_unblocked_user(self):
        self.check_request(self.api_client.get_user_unblocked, self.testing_user_data["username"], 304)

        self.check_user_access_status(self.testing_user_data["email"], 1)

    def test_unblock_non_existent_user(self, faker):
        non_existent_username = faker.pystr(max_chars=20, min_chars=0)

        self.check_request(self.api_client.get_user_unblocked, non_existent_username, 404)

    @pytest.mark.parametrize("api_url", [
        Links.APP_API_BLOCK_USER_PART, Links.APP_API_UNBLOCK_USER_PART, Links.APP_API_DELETE_USER_PART
    ])
    def test_unauthorized_get_requests(self, api_url):
        request_url = urljoin(Links.APP_BASE_LINK, f"{api_url}{self.testing_user_data['username']}")
        response = requests.get(request_url)

        assert response.status_code == 401

    def test_unauthorized_create_user_request(self):
        user_data = self.user_builder.create_user_data()
        request_url = urljoin(Links.APP_BASE_LINK, Links.APP_API_ADD_USER_PART)
        response = requests.post(request_url, json=user_data)

        assert response.status_code == 401
