from selenium.webdriver.common.by import By


class LoginLocators:

    OPEN_LOGIN_MODAL_BUTTON = (
        By.XPATH, '//div[contains(@class, "responseHead-module-button")]'
    )
    EMAIL_INPUT = (
        By.NAME, 'email'
    )
    PASSWORD_INPUT = (
        By.NAME, 'password'
    )
    LOGIN_SUBMIT_BUTTON = (
        By.XPATH, '//div[contains(@class, "authForm-module-button")]'
    )
