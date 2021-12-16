import pytest

from static.error_messages import ErrorMessages
from static.links import Links
from static.tests_config import TestsConfig
from tests.ui_tests.base_ui import BaseCaseUI


class TestRegister(BaseCaseUI):

    @pytest.fixture(scope='function', autouse=True)
    def setup_tests(self):
        self.register_page = self.login_page.go_to_register_page()
        self.error_block_locator = self.register_page.locators.ERROR_MESSAGE

    def register_user(self, username_size=None, email_prefix_size=None, password_size=None,
                      correct_email=True, confirm_password=None, click_checkbox=True):
        user_data = self.user_builder.create_user_data(username_size, email_prefix_size, password_size, correct_email)
        self.register_page.register(user_data["username"], user_data["email"], user_data["password"],
                                    confirm_password, click_checkbox)
        return user_data

    def check_entity_existence(self, field, field_value, not_exist=True):
        user_entity = self.mysql_client.get_user(field, field_value)
        if not_exist:
            assert user_entity is None
        else:
            assert user_entity is not None
            assert user_entity.access == 1

    def test_correct_register(self):
        user_data = self.register_user()

        assert self.driver.current_url == Links.APP_MAIN_PAGE
        self.check_entity_existence("email", user_data["email"], not_exist=False)

        self.mysql_client.delete_user(user_data["email"])

    def test_set_active_and_start_time_values(self):
        user_data = self.register_user()

        user_entity = self.mysql_client.get_user("email", user_data["email"])
        assert user_entity.active == 1 and user_entity.start_active_time is not None

    @pytest.mark.parametrize(
        "data_for_register,message_to_check,equal_flag",
        [
            ({"username_size": 5}, ErrorMessages.INCORRECT_USERNAME_LENGTH, True),
            ({"username_size": 17}, ErrorMessages.INCORRECT_USERNAME_LENGTH, True),
            ({"email_prefix_size": 1}, ErrorMessages.INCORRECT_EMAIL_LENGTH, True),
            ({"email_prefix_size": 64}, ErrorMessages.INCORRECT_EMAIL_LENGTH, True),
            ({"username_size": 0}, None, True),
            ({"email_prefix_size": 0}, ErrorMessages.INCORRECT_EMAIL_LENGTH, True),
            ({"password_size": 0}, None, True),
            ({"confirm_password": ''}, ErrorMessages.PASSWORD_MUST_MATCH, True),
            ({"password_size": 5}, None, True),
            ({"password_size": 256}, ErrorMessages.INTERNAL_SERVER_ERROR, False)
        ]
    )
    def test_parameters_incorrect_length(self, faker, data_for_register, message_to_check, equal_flag):
        if data_for_register.get("password_size", None) == 0:
            data_for_register["confirm_password"] = faker.unique.pystr(max_chars=6)
        user_data = self.register_user(**data_for_register)

        if message_to_check is None:
            assert self.driver.current_url == Links.APP_REGISTER_PAGE
        else:
            self.check_error_message(self.register_page, self.error_block_locator, message_to_check, equal=equal_flag)
        self.check_entity_existence("email", user_data["email"])

    def test_without_term_check(self):
        user_data = self.register_user(click_checkbox=False)

        assert self.driver.current_url == Links.APP_REGISTER_PAGE
        self.check_entity_existence("email", user_data["email"])

    def test_incorrect_email_format(self):
        user_data = self.register_user(correct_email=False)

        self.check_error_message(self.register_page, self.error_block_locator, ErrorMessages.INVALID_EMAIL_ADDRESS)
        self.check_entity_existence("email", user_data["email"])

    def test_passwords_not_match(self, faker):
        user_data = self.register_user(confirm_password=faker.unique.pystr(max_chars=8))

        self.check_error_message(self.register_page, self.error_block_locator, ErrorMessages.PASSWORD_MUST_MATCH)
        self.check_entity_existence("email", user_data["email"])

    def test_two_and_more_errors(self, faker):
        user_data = self.register_user(
            correct_email=False,
            confirm_password=faker.unique.pystr(max_chars=8)
        )

        self.check_entity_existence("email", user_data["email"])
        error_block = self.register_page.find(self.register_page.locators.ERROR_MESSAGE)
        assert TestsConfig.DANGER_MESSAGE_STYLE in error_block.get_attribute('class')

    @pytest.mark.parametrize(
        "field_to_change,message_to_check,equal_flag",
        [
            ("email", ErrorMessages.USER_ALREADY_EXIST, True),
            ("username", ErrorMessages.INTERNAL_SERVER_ERROR, False),
        ]
    )
    def test_add_user_with_same_field(self, faker, field_to_change, message_to_check, equal_flag):
        user_data = self.user_builder.create_user_data()
        self.mysql_client.add_user(user_data)
        user_data[field_to_change] = faker.unique.pystr(max_chars=16)
        if field_to_change == 'email':
            user_data[field_to_change] += '@a.a'
        self.register_page.register(user_data["username"], user_data["email"], user_data["password"])

        self.check_error_message(self.register_page, self.error_block_locator, message_to_check, equal_flag)
        self.check_entity_existence(field_to_change, user_data[field_to_change])
