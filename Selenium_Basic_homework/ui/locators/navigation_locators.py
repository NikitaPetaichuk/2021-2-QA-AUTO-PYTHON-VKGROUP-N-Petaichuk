from selenium.webdriver.common.by import By


class NavigationLocators:

    GO_TO_CAMPAIGNS_BUTTON = (
        By.XPATH, '//a[contains(@class, "center-module-campaigns")]'
    )
    GO_TO_PROFILE_BUTTON = (
        By.XPATH, '//a[contains(@class, "center-module-profile")]'
    )
    GO_TO_TOOLS_BUTTON = (
        By.XPATH, '//a[contains(@class, "center-module-tools")]'
    )
