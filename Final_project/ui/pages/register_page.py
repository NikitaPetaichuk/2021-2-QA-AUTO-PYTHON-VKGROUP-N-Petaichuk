from ui.locators.register_page_locators import RegisterPageLocators
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage


class RegisterPage(BasePage):

    locators = RegisterPageLocators()

    def register(self, username, email, password, confirm_password=None, click_checkbox=True):
        self.logger.info(f"Register account with credentials ({username}, {email}, {password})")

        if username is not None:
            self.write_into_input(self.locators.USERNAME_INPUT, username)
        if email is not None:
            self.write_into_input(self.locators.EMAIL_INPUT, email)
        if password is not None:
            self.write_into_input(self.locators.PASSWORD_INPUT, password)
        confirm_password = password if confirm_password is None else confirm_password
        if confirm_password is not None:
            self.write_into_input(self.locators.CONFIRM_PASSWORD_INPUT, confirm_password)
        if click_checkbox:
            self.click(self.locators.TERM_CHECKBOX)

        self.click(self.locators.REGISTER_BUTTON)
        return MainPage(self.driver)
