from selenium.webdriver.common.by import By


class LoginPageLocators:

    USERNAME_INPUT = (By.NAME, 'username')
    PASSWORD_INPUT = (By.NAME, 'password')
    LOGIN_BUTTON = (By.NAME, 'submit')
    REGISTER_LINK = (By.XPATH, '//a[@href = "/reg"]')
    ERROR_MESSAGE = (By.ID, 'flash')
