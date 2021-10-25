import allure
import pytest

from base import BaseCase
from static.tests_config import TestsConfig
from utils.generate_funcs import generate_spaces_string, generate_invalid_password
from ui.locators.error_login_locators import ErrorLoginLocators


class TestHomeworkTwoUnauthorized(BaseCase):

    authorize = False

    @allure.epic('QA Python Homework 2: Advanced UI testing')
    @allure.feature('Login negative tests')
    @allure.story('Use spaces for password')
    @pytest.mark.UI
    def test_login_using_spaces_as_password(self):
        with allure.step("Trying to log in using spaces as password"):
            self.login_page.login(TestsConfig.LOGIN_EMAIL, generate_spaces_string())
            login_error_block = self.login_page.find(self.login_page.locators.LOGIN_ERROR_BLOCK)
            assert login_error_block.is_displayed()

    @allure.epic('QA Python Homework 2: Advanced UI testing')
    @allure.feature('Login negative tests')
    @allure.story('Use invalid password')
    @pytest.mark.UI
    def test_login_invalid_password(self):
        with allure.step("Trying to log in using invalid password"):
            self.login_page.login(TestsConfig.LOGIN_EMAIL, generate_invalid_password())
            self.login_page.find(ErrorLoginLocators.ERROR_PAGE_LOGIN_FORM)
            assert self.driver.current_url.startswith(TestsConfig.INVALID_LOGIN_PAGE_URL_PREFIX)
