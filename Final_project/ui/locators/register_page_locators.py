from selenium.webdriver.common.by import By


class RegisterPageLocators:

    USERNAME_INPUT = (By.NAME, 'username')
    EMAIL_INPUT = (By.NAME, 'email')
    PASSWORD_INPUT = (By.NAME, 'password')
    CONFIRM_PASSWORD_INPUT = (By.NAME, 'confirm')
    TERM_CHECKBOX = (By.NAME, 'term')
    REGISTER_BUTTON = (By.NAME, 'submit')
    ERROR_MESSAGE = (By.ID, 'flash')
