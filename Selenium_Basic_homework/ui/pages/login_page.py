from ui.pages.base_page import BasePage
from ui.locators.login_locators import LoginLocators


EMAIL = 'pet.ai.4.uk@yandex.ru'
PASSWORD = 'TestAccount123'


class LoginPage(BasePage):

    locators = LoginLocators()

    def login(self):
        self.click(self.locators.OPEN_LOGIN_MODAL_BUTTON)
        email_input = self.find(self.locators.EMAIL_INPUT)
        password_input = self.find(self.locators.PASSWORD_INPUT)
        email_input.send_keys(EMAIL)
        password_input.send_keys(PASSWORD)
        self.click(self.locators.LOGIN_SUBMIT_BUTTON)
