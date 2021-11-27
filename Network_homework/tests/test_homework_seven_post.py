import allure
import pytest

from tests.base import BaseCase
from mock_service.mock_app import users_storage


class TestHomeworkSevenPost(BaseCase):

    @allure.epic('QA Python Homework 7: Mock testing')
    @allure.feature('POST request')
    @allure.story("Sending correct request")
    @pytest.mark.Mock
    def test_post_correct(self):
        with allure.step("Generating data for request"):
            data_to_send = self.user_builder.create_user_data()

        with allure.step("Sending request and getting response"):
            response = self.client.make_request(
                "POST", "/users/",
                headers={
                    "Content-Type": "application/json; charset=utf-8"
                },
                body=data_to_send
            )["body"]

        with allure.step("Checking response and mock state"):
            self._check_ok_response(response, "id")
            assert response["id"] in users_storage
            self._check_user_equality(users_storage[response["id"]], data_to_send)

    @allure.epic('QA Python Homework 7: Mock testing')
    @allure.feature('POST request')
    @allure.story("Sending incorrect request: sending non-JSON data")
    @pytest.mark.Mock
    def test_post_not_json(self):
        with allure.step("Generating data for request"):
            data_to_send = self.user_builder.create_user_data()

        with allure.step("Sending request and getting response"):
            response = self.client.make_request(
                "POST", "/users/",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
                },
                body=data_to_send
            )

        with allure.step("Checking error response"):
            self._check_error_response(response, 400, "Expected JSON data, got non-JSON data")

    @allure.epic('QA Python Homework 7: Mock testing')
    @allure.feature('POST request')
    @allure.story("Sending incorrect request: sending JSON data without required field")
    @pytest.mark.Mock
    @pytest.mark.parametrize(
        "json_field",
        [
            pytest.param("name"),
            pytest.param("surname")
        ]
    )
    def test_post_no_json_field(self, json_field):
        with allure.step("Generating data for request"):
            data_to_send = self.user_builder.create_user_data()
            del data_to_send[json_field]

        with allure.step("Sending request and getting response"):
            response = self.client.make_request(
                "POST", "/users/",
                headers={
                    "Content-Type": "application/json; charset=utf-8"
                },
                body=data_to_send
            )

        with allure.step("Checking error response"):
            self._check_error_response(response, 400,
                                       f"Incorrect JSON format: field '{json_field}' doesn't found")
