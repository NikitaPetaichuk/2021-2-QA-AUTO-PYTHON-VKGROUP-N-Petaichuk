from ui.locators.login_page_locators import LoginPageLocators
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.register_page import RegisterPage


class LoginPage(BasePage):

    locators = LoginPageLocators()

    def go_to_register_page(self):
        self.logger.info(f"Going into register page")

        self.click(self.locators.REGISTER_LINK)
        return RegisterPage(self.driver)

    def login(self, username=None, password=None):
        self.logger.info(f"Logging into app with credentials ({username}, {password})")

        if username is not None:
            self.write_into_input(self.locators.USERNAME_INPUT, username)
        if password is not None:
            self.write_into_input(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.LOGIN_BUTTON)
        return MainPage(self.driver)
