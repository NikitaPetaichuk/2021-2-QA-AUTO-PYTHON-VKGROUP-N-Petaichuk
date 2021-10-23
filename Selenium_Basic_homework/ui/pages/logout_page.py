from ui.pages.base_page import BasePage
from ui.locators.logout_locators import LogoutLocators


class LogoutPage(BasePage):

    locators = LogoutLocators()

    def logout(self):
        self.click(self.locators.USER_ACCOUNT_BUTTON)
        self.find(self.locators.OPENED_USER_MENU)
        self.click(self.locators.LOGOUT_BUTTON)
