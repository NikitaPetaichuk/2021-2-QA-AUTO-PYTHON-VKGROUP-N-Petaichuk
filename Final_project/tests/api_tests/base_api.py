import pytest

from api_clients.app_api_client import AppAPIClient, UnexpectedResponseStatusCodeException
from static.links import Links


class BaseCaseAPI:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, logger, mysql_client, user_builder, faker):
        self.user_builder = user_builder
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

    def check_request(self, request_method, request_data, expected_status=200):
        try:
            request_method(request_data, expected_status)
        except UnexpectedResponseStatusCodeException:
            user_entity = None
            if request_method is self.api_client.post_register_client:
                field = "email" if request_data.get("email", False) else "username"
                user_entity = self.mysql_client.get_user(field, request_data[field])
            elif request_method is self.api_client.get_user_delete:
                user_entity = self.mysql_client.get_user("username", request_data)

            if user_entity is not None:
                self.mysql_client.delete_user(user_entity.email)
            assert False, "Incorrect status code"
