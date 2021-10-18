from static.tests_config import TestsConfig
from ui.pages.base_page import BasePage
from ui.locators.login_locators import LoginLocators


class LoginPage(BasePage):

    locators = LoginLocators()

    def login(self):
        self.click(self.locators.OPEN_LOGIN_MODAL_BUTTON)
        email_input = self.find(self.locators.EMAIL_INPUT)
        password_input = self.find(self.locators.PASSWORD_INPUT)
        email_input.send_keys(TestsConfig.LOGIN_EMAIL)
        password_input.send_keys(TestsConfig.LOGIN_PASSWORD)
        self.click(self.locators.LOGIN_SUBMIT_BUTTON)
