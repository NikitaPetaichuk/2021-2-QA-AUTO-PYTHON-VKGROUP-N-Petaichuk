from urllib.parse import urljoin

import allure
import pytest
import requests

from static.links import Links
from tests.api_tests.base_api import BaseCaseAPI


class TestUserAccess(BaseCaseAPI):

    @pytest.fixture(scope='function', autouse=True)
    def setup_user_for_testing(self):
        """
        Setting up: Create user and add him to DB.
        Tearing down: Delete user from DB.
        """
        user_data = self.user_builder.create_user_data()
        self.mysql_client.add_user(user_data)
        self.testing_user_data = user_data
        yield
        self.mysql_client.delete_user(user_data["email"])

    def check_user_access_status(self, user_email, access_status):
        user_entity = self.mysql_client.get_user("email", user_email)
        assert user_entity.access == access_status, "Incorrect access state"

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User access API functionality')
    @allure.story('Blocking access for user')
    def test_block_user(self):
        """
        Test for checking blocking access for user.
        Steps:
        1. Blocking access for user using API.
        2. Check user access flag in DB.
        Expected result:
        Response status code 200, user access flag in DB equals 0.
        """
        with allure.step('Blocking access for user using API'):
            self.check_request(self.api_client.get_user_blocked, self.testing_user_data["username"])

        with allure.step('Check user access flag in DB'):
            self.check_user_access_status(self.testing_user_data["email"], 0)

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User access API functionality')
    @allure.story('Blocking access for blocked user')
    def test_block_blocked_user(self):
        """
        Test for checking blocking access for blocked user.
        Steps:
        1. Blocking access for user by updating DB.
        2. Blocking access for user using API.
        3. Check user access flag in DB.
        Expected result:
        Response status code 304, user access flag in DB equals 0.
        """
        with allure.step('Blocking access for user by updating DB'):
            self.mysql_client.set_user_access(self.testing_user_data["email"], 0)

        with allure.step('Blocking access for user using API'):
            self.check_request(self.api_client.get_user_blocked, self.testing_user_data["username"], 304)

        with allure.step('Check user access flag in DB'):
            self.check_user_access_status(self.testing_user_data["email"], 0)

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User access API functionality')
    @allure.story('Blocking access for non-existent user')
    def test_block_non_existent_user(self, faker):
        """
        Test for checking blocking access for non-existent user.
        Steps:
        1. Creating non-existent username.
        2. Blocking access for user using API.
        Expected result:
        Response status code 404.
        """
        with allure.step('Creating non-existent username'):
            non_existent_username = self.user_builder.create_user_data_string(20, 0)

        with allure.step('Blocking access for user using API'):
            self.check_request(self.api_client.get_user_blocked, non_existent_username, 404)

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User access API functionality')
    @allure.story('Unblocking access for user')
    def test_unblock_user(self):
        """
        Test for checking unblocking access for user.
        Steps:
        1. Blocking access for user by updating DB.
        2. Unblocking access for user using API.
        3. Check user access flag in DB.
        Expected result:
        Response status code 200, user access flag in DB equals 1.
        """
        with allure.step('Blocking access for user by updating DB'):
            self.mysql_client.set_user_access(self.testing_user_data["email"], 0)

        with allure.step('Unblocking access for user using API'):
            self.check_request(self.api_client.get_user_unblocked, self.testing_user_data["username"])

        with allure.step('Check user access flag in DB'):
            self.check_user_access_status(self.testing_user_data["email"], 1)

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User access API functionality')
    @allure.story('Unblocking access for unblocked user')
    def test_unblock_unblocked_user(self):
        """
        Test for checking unblocking access for unblocked user.
        Steps:
        1. Unblocking access for user (by default user is unblocked) using API.
        2. Check user access flag in DB.
        Expected result:
        Response status code 304, user access flag in DB equals 1.
        """
        with allure.step('Unblocking access for user using API'):
            self.check_request(self.api_client.get_user_unblocked, self.testing_user_data["username"], 304)

        with allure.step('Check user access flag in DB'):
            self.check_user_access_status(self.testing_user_data["email"], 1)

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User access API functionality')
    @allure.story('Unblocking access for non-existent user')
    def test_unblock_non_existent_user(self, faker):
        """
        Test for checking unblocking access for non-existent user.
        Steps:
        1. Creating non-existent username.
        2. Unblocking access for user using API.
        Expected result:
        Response status code 404.
        """
        with allure.step('Creating non-existent username'):
            non_existent_username = self.user_builder.create_user_data_string(20, 0)

        with allure.step('Unblocking access for user using API'):
            self.check_request(self.api_client.get_user_unblocked, non_existent_username, 404)

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User access API functionality')
    @allure.story('Checking API GET requests from unauthorized user')
    @pytest.mark.parametrize("api_url", [
        Links.APP_API_BLOCK_USER_PART, Links.APP_API_UNBLOCK_USER_PART, Links.APP_API_DELETE_USER_PART
    ])
    def test_unauthorized_get_requests(self, api_url):
        """
        Test for checking API GET requests from unauthorized user.
        Steps:
        1. Making request without authorization.
        2. Checking response status code.
        Expected result:
        Response status code 401.
        """
        with allure.step('Making request without authorization'):
            request_url = urljoin(Links.APP_BASE_LINK, f"{api_url}{self.testing_user_data['username']}")
            response = requests.get(request_url)

        with allure.step('Checking response status code'):
            assert response.status_code == 401, f"Unexpected response status code '{response.status_code}'"

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User access API functionality')
    @allure.story('Checking API create user request from unauthorized user')
    def test_unauthorized_create_user_request(self):
        """
        Test for checking API create user request from unauthorized user.
        Steps:
        1. Creating data for create user request.
        2. Making create user request without authorization.
        3. Checking response status code.
        Expected result:
        Response status code 401.
        """
        with allure.step('Creating data for create user request'):
            user_data = self.user_builder.create_user_data()

        with allure.step('Making create user request without authorization'):
            request_url = urljoin(Links.APP_BASE_LINK, Links.APP_API_ADD_USER_PART)
            response = requests.post(request_url, json=user_data)

        with allure.step('Checking response status code'):
            assert response.status_code == 401, f"Unexpected response status code '{response.status_code}'"
