from selenium.webdriver.common.by import By


class LogoutLocators:

    USER_ACCOUNT_BUTTON = (
        By.XPATH, '//div[contains(@class, "right-module-mail")]'
    )
    OPENED_USER_MENU = (
        By.XPATH, '//ul[contains(@class, "rightMenu-module-visibleRightMenu")]'
    )
    LOGOUT_BUTTON = (
        By.XPATH, '//a[contains(@class, "rightMenu-module-rightMenuLink") and contains(text(), "Выйти")]'
    )
