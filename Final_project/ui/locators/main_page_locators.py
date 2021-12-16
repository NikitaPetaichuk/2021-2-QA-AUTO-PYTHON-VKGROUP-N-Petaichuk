from selenium.webdriver.common.by import By


class MainPageLocators:

    @staticmethod
    def get_link_locator(url):
        return By.XPATH, f'//a[@href = "{url}"]'

    BRAND_LOGO = (By.XPATH, '//a[contains(@class, "uk-navbar-brand")]')
    HOME_BUTTON = (By.XPATH, '//li/a[@href = "/"]')
    PYTHON_BUTTON = (By.XPATH, '//li[2]/a')
    LINUX_BUTTON = (By.XPATH, '//li[3]/a')
    NETWORK_BUTTON = (By.XPATH, '//li[4]/a')

    USERNAME_LABEL = (By.XPATH, '//div[@id = "login-name"]//li[1]')
    VK_ID_LABEL = (By.XPATH, '//div[@id = "login-name"]//li[2]')
    LOGOUT_BUTTON = (By.ID, 'logout')
