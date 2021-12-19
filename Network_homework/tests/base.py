import pytest

from socket_client.client import SocketClient
from static.tests_config import TestsConfig
from utils.builders.user_builder import UserBuilder
from mock_service.mock_app import users_storage as users_storage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, logger):
        self.logger = logger
        self.user_builder = UserBuilder()
        self.client: SocketClient = SocketClient(TestsConfig.MOCK_HOST, TestsConfig.MOCK_PORT)

        self.logger.info("Initial setup completed")

    def _create_user_in_mock(self, min_id, max_id):
        user = self.user_builder.create_user_entity(min_id, max_id)
        users_storage[user["id"]] = user["data"]
        return user

    @staticmethod
    def _check_ok_response(response, json_additional_field=None, additional_field_keys=None):
        assert response.get("status", False)
        assert response["status"] == "ok"
        if json_additional_field is not None:
            assert response.get(json_additional_field, False)
            if additional_field_keys is not None:
                for key in additional_field_keys:
                    assert response[json_additional_field].get(key, False)

    @staticmethod
    def _check_error_response(response, status_code, error_message):
        assert response["status_code"] == status_code
        json_response = response["body"]
        assert json_response.get("status", False)
        assert json_response["status"] == "error"
        assert json_response.get("message", False)
        assert json_response["message"] == error_message

    @staticmethod
    def _check_user_equality(user_one, user_two):
        assert user_one["name"] == user_two["name"]
        assert user_one["surname"] == user_two["surname"]
