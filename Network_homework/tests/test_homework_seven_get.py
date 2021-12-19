import allure
import pytest

from mock_service.mock_app import users_storage
from tests.base import BaseCase
from utils.util_funcs import generate_non_existing_key


class TestHomeworkSevenGet(BaseCase):

    @allure.epic('QA Python Homework 7: Mock testing')
    @allure.feature('GET request')
    @allure.story('Sending correct request')
    @pytest.mark.Mock
    def test_get_correct(self):
        with allure.step("Setting up testing environment"):
            user = self._create_user_in_mock(100, 200)

        with allure.step("Sending request and getting response"):
            response = self.client.make_request("GET", f"/users/{user['id']}")["body"]

        with allure.step("Checking response"):
            self._check_ok_response(response, "user", ["name", "surname"])
            self._check_user_equality(response["user"], user["data"])

    @allure.epic('QA Python Homework 7: Mock testing')
    @allure.feature('GET request')
    @allure.story("Sending incorrect request: user doesn't exist")
    @pytest.mark.Mock
    def test_get_user_not_exist(self):
        with allure.step("Generating data for request"):
            non_existing_key = generate_non_existing_key(users_storage.keys())

        with allure.step("Sending request and getting response"):
            response = self.client.make_request("GET", f"/users/{non_existing_key}")

        with allure.step("Checking error response"):
            self._check_error_response(response, 404,
                                       f"User with identifier '{non_existing_key}' doesn't exist")
