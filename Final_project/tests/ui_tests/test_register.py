import allure
import pytest

from static.error_messages import ErrorMessages
from static.links import Links
from static.tests_config import TestsConfig
from tests.ui_tests.base_ui import BaseCaseUI


class TestRegister(BaseCaseUI):

    @pytest.fixture(scope='function', autouse=True)
    def setup_tests(self):
        """
        Setting up: going to register page and getting html element locator for error messages
        """
        self.register_page = self.login_page.go_to_register_page()
        self.error_block_locator = self.register_page.locators.ERROR_MESSAGE

    def register_user(self, username_size=None, email_prefix_size=None, password_size=None,
                      correct_email=True, confirm_password=None, click_checkbox=True):
        """
        Registering user:
        1. Creating user data.
        2. Using user data for filling register form and submitting registering
        """
        user_data = self.user_builder.create_user_data(username_size, email_prefix_size, password_size, correct_email)
        self.register_page.register(user_data["username"], user_data["email"], user_data["password"],
                                    confirm_password, click_checkbox)
        return user_data

    def check_entity_existence(self, field, field_value, not_exist=True):
        user_entity = self.mysql_client.get_user(field, field_value)
        if not_exist:
            assert user_entity is None, "Unexpected entity existence"
        else:
            assert user_entity is not None, "Unexpected entity non-existence"
            assert user_entity.access == 1, "Unexpected entity access state"

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App register functionality')
    @allure.story('Checking correct user register')
    def test_correct_register(self):
        """
        Test for checking correct user register.
        Steps:
        1. Registering user.
        2. Checking current url and user data existence in DB.
        Expected result:
        User is successfully registered (user data added to DB), going to the main page.
        """
        with allure.step('Registering user'):
            user_data = self.register_user()

        with allure.step('Checking current url and user data existence in DB'):
            assert self.driver.current_url == Links.APP_MAIN_PAGE
            self.check_entity_existence("email", user_data["email"], not_exist=False)

        with allure.step('Tearing down: deleting user from DB'):
            self.mysql_client.delete_user(user_data["email"])

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App register functionality')
    @allure.story('Checking active user status after registering')
    def test_set_active_and_start_time_values(self):
        """
        Test for checking active user status after registering.
        Steps:
        1. Registering user.
        2. Checking user active state and start time value.
        Expected result:
        User active state is 1, start time value is not NULL.
        """
        with allure.step('Registering user'):
            user_data = self.register_user()

        with allure.step('Checking user active state and start time value'):
            user_entity = self.mysql_client.get_user("email", user_data["email"])
            assert user_entity.active == 1 and user_entity.start_active_time is not None, "Incorrect active " \
                                                                                          "state/start time value"

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App register functionality')
    @allure.story('Checking user register using values with incorrect length')
    @pytest.mark.parametrize(
        "data_for_register,message_to_check,equal_flag",
        [
            ({"username_size": 5}, ErrorMessages.INCORRECT_USERNAME_LENGTH, True),
            ({"username_size": 17}, ErrorMessages.INCORRECT_USERNAME_LENGTH, True),
            ({"email_prefix_size": 1}, ErrorMessages.INCORRECT_EMAIL_LENGTH, True),
            ({"email_prefix_size": 61}, ErrorMessages.INCORRECT_EMAIL_LENGTH, True),
            ({"username_size": 0}, None, True),
            ({"email_prefix_size": 0}, ErrorMessages.INCORRECT_EMAIL_LENGTH, True),
            ({"password_size": 0}, None, True),
            ({"confirm_password": ''}, ErrorMessages.PASSWORD_MUST_MATCH, True),
            ({"password_size": 5}, None, True),
            ({"password_size": 256}, ErrorMessages.INTERNAL_SERVER_ERROR, False)
        ]
    )
    def test_parameters_incorrect_length(self, faker, data_for_register, message_to_check, equal_flag):
        """
        Test for checking user register using values with incorrect length.
        Steps:
        1. Registering user with given data settings.
        2. Checking page state and user data existence in DB.
        Expected result:
        Correct error message is shown OR Incorrect message isn't shown OR Current url is register url.
        User data is not added to DB.
        """
        with allure.step('Registering user with given data settings'):
            if data_for_register.get("password_size", None) == 0:
                data_for_register["confirm_password"] = faker.unique.pystr(max_chars=6)
            user_data = self.register_user(**data_for_register)

        with allure.step('Checking page state and user data existence in DB'):
            if message_to_check is None:
                assert self.driver.current_url == Links.APP_REGISTER_PAGE, f"Incorrect current url " \
                                                                           f"'{self.driver.current_url}'"
            else:
                self.check_error_message(
                    self.register_page, self.error_block_locator, message_to_check, equal=equal_flag
                )
            self.check_entity_existence("email", user_data["email"])

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App register functionality')
    @allure.story('Checking user register without term checking')
    def test_without_term_check(self):
        """
        Test for checking user register without term checking.
        Steps:
        1. Registering user without term checking.
        2. Checking current url and user data existence in DB.
        Expected result:
        Current url is register url, user data is not added to DB.
        """
        with allure.step('Registering user without term checking'):
            user_data = self.register_user(click_checkbox=False)

        with allure.step('Checking current url and user data existence in DB'):
            assert self.driver.current_url == Links.APP_REGISTER_PAGE, f"Incorrect current url " \
                                                                       f"'{self.driver.current_url}'"
            self.check_entity_existence("email", user_data["email"])

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App register functionality')
    @allure.story('Checking user register with invalid email')
    def test_incorrect_email_format(self):
        """
        Test for checking user register with invalid email.
        Steps:
        1. Registering user with invalid email.
        2. Checking error message and user data existence in DB.
        Expected result:
        Correct error message is shown, user data is not added to DB.
        """
        with allure.step('Registering user with invalid email'):
            user_data = self.register_user(correct_email=False)

        with allure.step('Checking error message and user data existence in DB'):
            self.check_error_message(self.register_page, self.error_block_locator, ErrorMessages.INVALID_EMAIL_ADDRESS)
            self.check_entity_existence("email", user_data["email"])

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App register functionality')
    @allure.story('Checking user register with not matching passwords')
    def test_passwords_not_match(self):
        """
        Test for checking user register with not matching passwords.
        Steps:
        1. Registering user with not matching passwords.
        2. Checking error message and user data existence in DB.
        Expected result:
        Correct error message is shown, user data is not added to DB.
        """
        with allure.step('Registering user with not matching passwords'):
            user_data = self.register_user(confirm_password=self.user_builder.create_user_data_string(8))

        with allure.step('Checking error message and user data existence in DB'):
            self.check_error_message(self.register_page, self.error_block_locator, ErrorMessages.PASSWORD_MUST_MATCH)
            self.check_entity_existence("email", user_data["email"])

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App register functionality')
    @allure.story('Checking user register with two value errors')
    def test_two_and_more_errors(self):
        """
        Test for checking user register with two value errors.
        Steps:
        1. Registering user with two value errors.
        2. Checking error message and user data existence in DB.
        Expected result:
        Error message block has correct style, user data is not added to DB.
        """
        with allure.step('Registering user with two value errors'):
            user_data = self.register_user(
                correct_email=False,
                confirm_password=self.user_builder.create_user_data_string(8)
            )

        with allure.step('Checking error message and user data existence in DB'):
            self.check_entity_existence("email", user_data["email"])
            error_block = self.register_page.find(self.register_page.locators.ERROR_MESSAGE)
            assert TestsConfig.DANGER_MESSAGE_STYLE in error_block.get_attribute('class'), "Error message got " \
                                                                                           "incorrect style"

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App register functionality')
    @allure.story('Checking user register with existent field value')
    @pytest.mark.parametrize(
        "field_to_change,message_to_check,equal_flag",
        [
            ("email", ErrorMessages.USER_ALREADY_EXIST, True),
            ("username", ErrorMessages.INTERNAL_SERVER_ERROR, False),
        ]
    )
    def test_add_user_with_same_field(self, field_to_change, message_to_check, equal_flag):
        """
        Test for checking user register with two value errors.
        Steps:
        1. Creating first user and adding him to DB.
        2. Creating second user data by modifying first user data.
        3. Registering second user.
        4. Checking error message and user data existence in DB.
        Expected result:
        Correct error message is shown OR Incorrect error message isn't shown.
        User data is not added to DB.
        """
        with allure.step('Creating first user and adding him to DB'):
            user_data = self.user_builder.create_user_data()
            self.mysql_client.add_user(user_data)

        with allure.step('Creating second user data by modifying first user data'):
            changed_user_data = user_data.copy()
            changed_user_data[field_to_change] = self.user_builder.create_user_data_string(16)
            if field_to_change == 'email':
                changed_user_data[field_to_change] += '@a.a'

        with allure.step('Registering second user'):
            self.register_page.register(
                changed_user_data["username"],
                changed_user_data["email"],
                changed_user_data["password"]
            )

        with allure.step('Checking error message and user data existence in DB'):
            self.check_error_message(self.register_page, self.error_block_locator, message_to_check, equal_flag)
            self.check_entity_existence(field_to_change, changed_user_data[field_to_change])

        with allure.step('Tearing down: deleting first user from DB'):
            self.mysql_client.delete_user(user_data["email"])
