import allure
import pytest

from mock_service.mock_app import users_storage
from tests.base import BaseCase
from utils.util_funcs import generate_non_existing_key


class TestHomeworkSevenDelete(BaseCase):

    @allure.epic('QA Python Homework 7: Mock testing')
    @allure.feature('DELETE request')
    @allure.story('Sending correct request')
    @pytest.mark.Mock
    def test_delete_correct(self):
        with allure.step("Setting up testing environment"):
            user = self._create_user_in_mock(500, 600)

        with allure.step("Sending request and getting response"):
            response = self.client.make_request("DELETE", f"/users/{user['id']}")["body"]

        with allure.step("Checking response and mock state"):
            self._check_ok_response(response)
            assert user['id'] not in users_storage

    @allure.epic('QA Python Homework 7: Mock testing')
    @allure.feature('DELETE request')
    @allure.story("Sending incorrect request: user doesn't exist")
    @pytest.mark.Mock
    def test_delete_user_not_exist(self):
        with allure.step("Generating data for request"):
            non_existing_key = generate_non_existing_key(users_storage.keys())

        with allure.step("Sending request and getting response"):
            response = self.client.make_request("DELETE", f"/users/{non_existing_key}")

        with allure.step("Checking error response"):
            self._check_error_response(response, 404,
                                       f"User with identifier '{non_existing_key}' doesn't exist")
