from selenium.webdriver.common.by import By


class ToolsLocators:

    FEEDS_TITLE = (
        By.XPATH, '//div[contains(text(), "Список фидов")]'
    )
