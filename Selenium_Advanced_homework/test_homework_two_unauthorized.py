import allure
import pytest

from base import BaseCase
from static.tests_config import TestsConfig
from ui.locators.error_login_locators import ErrorLoginLocators


class TestHomeworkTwoUnauthorized(BaseCase):

    authorize = False

    @allure.epic('QA Python Homework 2: Advanced UI testing')
    @allure.feature('Login negative tests')
    @allure.story('Use spaces for password')
    @pytest.mark.UI
    def test_login_using_spaces_as_password(self, faker):
        with allure.step("Trying to log in using spaces as password"):
            spaced_password = ' ' * faker.pyint(min_value=1, max_value=10)
            self.login_page.login(TestsConfig.LOGIN_EMAIL, spaced_password)
            login_error_block = self.login_page.find(self.login_page.locators.LOGIN_ERROR_BLOCK)
            assert login_error_block.is_displayed()

    @allure.epic('QA Python Homework 2: Advanced UI testing')
    @allure.feature('Login negative tests')
    @allure.story('Use invalid password')
    @pytest.mark.UI
    def test_login_invalid_password(self, faker):
        with allure.step("Trying to log in using invalid password"):
            invalid_password = faker.pystr(min_chars=6, max_chars=10)
            self.login_page.login(TestsConfig.LOGIN_EMAIL, invalid_password)
            error_message = self.login_page.find(ErrorLoginLocators.ERROR_LOGIN_MESSAGE)
            assert error_message.is_displayed()
            assert error_message.text == TestsConfig.INVALID_LOGIN_MESSAGE

