import allure
import pytest

from static.error_messages import ErrorMessages
from static.links import Links
from tests.ui_tests.base_ui import BaseCaseUI


class TestLogin(BaseCaseUI):

    @pytest.fixture(scope='function', autouse=True)
    def setup_tests(self):
        """
        Setting up: getting html element locator for error messages
        """
        self.error_block_locator = self.login_page.locators.ERROR_MESSAGE

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App login functionality')
    @allure.story('Checking correct user logging in')
    def test_correct_login(self, faker):
        """
        Test for checking correct user logging in.
        Steps:
        1. User logging in.
        2. Checking current url, user access and active state and start time value.
        Expected result:
        User is successfully logged in, going to the main page.
        Access state is 1, active state is 1, start time value is not NULL.
        """
        with allure.step('User logging in'):
            user_data, _ = self.login_new_user(faker, False)

        with allure.step('Checking current url, user access and active state and start time value'):
            assert self.driver.current_url == Links.APP_MAIN_PAGE, f"Incorrect current url '{self.driver.current_url}'"
            user_entity = self.mysql_client.get_user("email", user_data["email"])
            assert user_entity.access == 1, "Incorrect access status"
            assert user_entity.active == 1 and user_entity.start_active_time is not None, "Incorrect active " \
                                                                                          "state/start time value"

        with allure.step('Tearing down: deleting user from DB.'):
            self.mysql_client.delete_user(user_data["email"])

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App login functionality')
    @allure.story('Checking going to register page')
    def test_go_to_register_page(self):
        """
        Test for checking correct user logging in.
        Steps:
        1. Going to register page.
        2. Checking current url.
        Expected result:
        Current url is register url.
        """
        with allure.step('Going to register page'):
            self.login_page.go_to_register_page()

        with allure.step('Checking current url'):
            assert self.driver.current_url == Links.APP_REGISTER_PAGE, f"Incorrect current url " \
                                                                       f"'{self.driver.current_url}'"

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App login functionality')
    @allure.story('Checking user logging in using values with incorrect length')
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
        """
        Test for checking user logging in using values with incorrect length.
        Steps:
        1. Creating user data with given settings.
        2. User logging in using created user data.
        3. Checking page state.
        Expected result:
        Current url is login url OR Correct message is shown OR Incorrect message isn't shown.
        """
        with allure.step('Creating user data with given settings'):
            user_data = self.user_builder.create_user_data(**data_for_login)

        with allure.step('User logging in using created user data'):
            self.login_page.login(user_data["username"], user_data["password"])

        with allure.step('Checking page state.'):
            if message_to_check is None:
                assert self.driver.current_url == Links.APP_SELENOID_BASE_LINK, f"Incorrect current url " \
                                                                                f"'{self.driver.current_url}'"
            else:
                self.check_error_message(self.login_page, self.error_block_locator, message_to_check, equal=equal_flag)

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App login functionality')
    @allure.story('Checking blocked user logging in')
    def test_blocked_user(self):
        """
        Test for checking blocked user logging in.
        Steps:
        1. Creating user data and adding it to DB.
        2. Blocking user.
        3. User logging in.
        4. Checking error message.
        Expected result:
        Correct message is shown.
        """
        with allure.step('Creating user data and adding it to DB'):
            user_data = self.user_builder.create_user_data()
            self.mysql_client.add_user(user_data)

        with allure.step('Blocking user'):
            self.mysql_client.set_user_access(user_data["email"], 0)

        with allure.step('User logging in'):
            self.login_page.login(user_data["username"], user_data["password"])

        with allure.step('Checking error message'):
            self.check_error_message(self.login_page, self.error_block_locator, ErrorMessages.ACCOUNT_BLOCKED)

        with allure.step('Tearing down: deleting user from DB.'):
            self.mysql_client.delete_user(user_data["email"])

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App login functionality')
    @allure.story('Checking user logging in with incorrect field')
    @pytest.mark.parametrize(
        "field_to_change",
        [
            "username",
            "password"
        ]
    )
    def test_incorrect_field(self, field_to_change):
        """
        Test for checking blocked user logging in.
        Steps:
        1. Creating user data and adding it to DB.
        2. Modifying one field of user data.
        3. User logging in.
        4. Checking error message.
        Expected result:
        Correct message is shown.
        """
        with allure.step('Creating user data and adding it to DB'):
            user_data = self.user_builder.create_user_data()
            self.mysql_client.add_user(user_data)

        with allure.step('Modifying one field of user data'):
            changed_user_data = user_data.copy()
            changed_user_data[field_to_change] = self.user_builder.create_user_data_string(16)

        with allure.step('User logging in'):
            self.login_page.login(changed_user_data["username"], changed_user_data["password"])

        with allure.step('Checking error message'):
            self.check_error_message(
                self.login_page, self.error_block_locator, ErrorMessages.INVALID_USERNAME_OR_PASSWORD
            )

        with allure.step('Tearing down: deleting user from DB.'):
            self.mysql_client.delete_user(user_data["email"])
