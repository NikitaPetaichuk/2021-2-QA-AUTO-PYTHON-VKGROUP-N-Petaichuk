import allure
import pytest

from mock_service.mock_app import users_storage
from tests.base import BaseCase
from utils.util_funcs import generate_non_existing_key


class TestHomeworkSevenPut(BaseCase):

    @allure.epic('QA Python Homework 7: Mock testing')
    @allure.feature('PUT request')
    @allure.story('Sending correct request')
    @pytest.mark.Mock
    def test_put_correct(self):
        with allure.step("Setting up testing environment"):
            user = self._create_user_in_mock(300, 400)

        with allure.step("Generating data for request"):
            data_to_send = self.user_builder.create_user_data()

        with allure.step("Sending request and getting response"):
            response = self.client.make_request(
                "PUT", f"/users/{user['id']}",
                headers={
                    "Content-Type": "application/json; charset=utf-8"
                },
                body=data_to_send
            )["body"]

        with allure.step("Checking response and mock state"):
            self._check_ok_response(response)
            self._check_user_equality(users_storage[user['id']], data_to_send)

    @allure.epic('QA Python Homework 7: Mock testing')
    @allure.feature('PUT request')
    @allure.story("Sending incorrect request: user doesn't exist")
    @pytest.mark.Mock
    def test_put_user_not_exist(self):
        with allure.step("Generating data for request"):
            non_existing_key = generate_non_existing_key(users_storage.keys())
            data_to_send = self.user_builder.create_user_data()

        with allure.step("Sending request and getting response"):
            response = self.client.make_request(
                "PUT", f"/users/{non_existing_key}",
                headers={
                    "Content-Type": "application/json; charset=utf-8"
                },
                body=data_to_send
            )

        with allure.step("Checking error response"):
            self._check_error_response(response, 404,
                                       f"User with identifier '{non_existing_key}' doesn't exist")

    @allure.epic('QA Python Homework 7: Mock testing')
    @allure.feature('PUT request')
    @allure.story("Sending incorrect request: sending non-JSON data")
    @pytest.mark.Mock
    def test_put_not_json(self):
        with allure.step("Setting up testing environment"):
            user = self._create_user_in_mock(700, 800)

        with allure.step("Generating data for request"):
            data_to_send = self.user_builder.create_user_data()

        with allure.step("Sending request and getting response"):
            response = self.client.make_request(
                "PUT", f"/users/{user['id']}",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
                },
                body=data_to_send
            )

        with allure.step("Checking error response"):
            self._check_error_response(response, 400, "Expected JSON data, got non-JSON data")
