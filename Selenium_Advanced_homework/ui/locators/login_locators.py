from selenium.webdriver.common.by import By


class LoginLocators:

    OPEN_LOGIN_MODAL_BUTTON = (
        By.XPATH, '//div[contains(@class, "responseHead-module-button")]'
    )
    LOGIN_MODAL_BODY = (
        By.XPATH, '//div[contains(@class, "mainPage-module-authModalBody")]'
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
    LOGIN_ERROR_BLOCK = (
        By.XPATH, '//div[contains(@class, "notify-module-error") and contains(@class, "notify-module-notifyBlock")]'
    )
