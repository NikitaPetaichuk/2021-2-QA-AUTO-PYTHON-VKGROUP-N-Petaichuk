import pytest

from api_clients.app_api_client import AppAPIClient, UnexpectedResponseStatusCodeException
from static.links import Links
from utils.user_builder import UserBuilder


class BaseCaseAPI:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, logger, mysql_client, faker):
        self.user_builder = UserBuilder()
        self.mysql_client = mysql_client
        self.logger = logger

        self.create_api_client(faker)
        self.api_client.post_register_client()

        self.logger.info("API testing initial setup is completed")

    def create_api_client(self, faker):
        username_size = faker.pyint(min_value=6, max_value=16)
        email_prefix_size = faker.pyint(min_value=2, max_value=60)
        password_size = faker.pyint(min_value=6, max_value=255)

        self.credentials = self.user_builder.create_user_data(username_size, email_prefix_size, password_size)
        self.api_client = AppAPIClient(Links.APP_BASE_LINK, self.credentials["username"], self.credentials["email"],
                                       self.credentials["password"])

    @staticmethod
    def check_request(request_method, request_data, expected_status=200):
        try:
            request_method(request_data, expected_status)
        except UnexpectedResponseStatusCodeException:
            assert False
