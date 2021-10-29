import logging
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, \
    TimeoutException
from static.tests_config import TestsConfig


class PageNotLoadedException(Exception):
    pass


class BasePage(object):

    url = 'https://target.my.com/'

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.logger = logging.getLogger('tests')
        self.is_opened()

    def is_opened(self, timeout=TestsConfig.DEFAULT_WAITING_TIMEOUT):
        start_loading_time = time.time()
        while time.time() - start_loading_time < timeout:
            if self.driver.current_url == self.url:
                return True
        raise PageNotLoadedException(f'{self.url} did not open in {timeout} sec for {self.__class__.__name__}.\n'
                                     f'Current url is {self.driver.current_url}.')

    def wait(self, timeout=None):
        if timeout is None:
            timeout = TestsConfig.DEFAULT_WAITING_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout=timeout).until(ec.visibility_of_element_located(locator))

    def find_hidden(self, locator, timeout=None):
        return self.wait(timeout=timeout).until(ec.presence_of_element_located(locator))

    def is_element_exists(self, locator, timeout=None):
        self.logger.debug(f"Checking if element with locator {locator} exists")
        try:
            self.find(locator, timeout=timeout)
            return True
        except TimeoutException:
            return False

    def click(self, locator, timeout=None):
        self.logger.debug(f"Clicking on element with locator {locator}")
        for attempt_number in range(TestsConfig.CLICK_ATTEMPTS_COUNT):
            try:
                element = self.find(locator, timeout=timeout)
                element.click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                if attempt_number == TestsConfig.CLICK_ATTEMPTS_COUNT - 1:
                    raise
