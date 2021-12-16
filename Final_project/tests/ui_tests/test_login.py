import pytest

from static.error_messages import ErrorMessages
from static.links import Links
from tests.ui_tests.base_ui import BaseCaseUI


class TestLogin(BaseCaseUI):

    @pytest.fixture(scope='function', autouse=True)
    def setup_tests(self):
        self.error_block_locator = self.login_page.locators.ERROR_MESSAGE

    def test_correct_login(self, faker):
        user_data, _ = self.login_new_user(faker)

        assert self.driver.current_url == Links.APP_MAIN_PAGE
        user_entity = self.mysql_client.get_user("email", user_data["email"])
        assert user_entity.access == 1
        assert user_entity.active == 1 and user_entity.start_active_time is not None

        self.mysql_client.delete_user(user_data["email"])

    def test_go_to_register_page(self):
        self.login_page.go_to_register_page()

        assert self.driver.current_url == Links.APP_REGISTER_PAGE

    @pytest.mark.parametrize(
        "data_for_login,message_to_check,equal_flag",
        [
            ({"username_size": 0}, None, True),
            ({"password_size": 0}, None, True),
            ({"username_size": 5}, ErrorMessages.INCORRECT_USERNAME_LENGTH, True),
            ({"username_size": 17}, ErrorMessages.INCORRECT_USERNAME_LENGTH, True),
            ({"password_size": 5}, ErrorMessages.INVALID_USERNAME_OR_PASSWORD, False),
            ({"password_size": 256}, ErrorMessages.INVALID_USERNAME_OR_PASSWORD, False)
        ]
    )
    def test_parameters_incorrect_length(self, data_for_login, message_to_check, equal_flag):
        user_data = self.user_builder.create_user_data(**data_for_login)
        self.login_page.login(user_data["username"], user_data["password"])

        if message_to_check is None:
            assert self.driver.current_url == Links.APP_BASE_LINK
        else:
            self.check_error_message(self.login_page, self.error_block_locator, message_to_check, equal=equal_flag)

    def test_blocked_user(self):
        user_data = self.user_builder.create_user_data()
        self.mysql_client.add_user(user_data)
        self.mysql_client.set_user_access(user_data["email"], 0)
        self.login_page.login(user_data["username"], user_data["password"])

        self.check_error_message(self.login_page, self.error_block_locator, ErrorMessages.ACCOUNT_BLOCKED)

        self.mysql_client.delete_user(user_data["email"])

    @pytest.mark.parametrize(
        "field_to_change",
        [
            "username",
            "password"
        ]
    )
    def test_incorrect_field(self, field_to_change, faker):
        user_data = self.user_builder.create_user_data()
        self.mysql_client.add_user(user_data)
        user_data[field_to_change] = faker.unique.pystr(max_chars=12)
        self.login_page.login(user_data["username"], user_data["password"])

        self.check_error_message(self.login_page, self.error_block_locator, ErrorMessages.INVALID_USERNAME_OR_PASSWORD)

        self.mysql_client.delete_user(user_data["email"])
