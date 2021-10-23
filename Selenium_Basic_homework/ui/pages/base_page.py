from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from static.tests_config import TestsConfig


class BasePage(object):

    url = 'https://target.my.com/'

    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout=timeout).until(ec.visibility_of_element_located(locator))

    def click(self, locator, timeout=None):
        for attempt_number in range(TestsConfig.CLICK_ATTEMPTS_COUNT):
            try:
                element = self.find(locator, timeout=timeout)
                element.click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                if attempt_number == TestsConfig.CLICK_ATTEMPTS_COUNT - 1:
                    raise
