import logging
import time

from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from static.links import Links
from static.tests_config import TestsConfig


class PageNotLoadedException(Exception):
    pass


class BasePage:

    url = Links.APP_BASE_LINK

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.logger = logging.getLogger('tests')

        self.logger.info(f'Going to {self.__class__.__name__}')
        self.is_opened()
        self.logger.info(f'{self.__class__.__name__} is active')

    def is_opened(self, timeout=TestsConfig.DEFAULT_WAITING_TIMEOUT):
        start_loading_time = time.time()
        while time.time() - start_loading_time < timeout:
            if self.driver.current_url.startswith(self.url):
                return True
        raise PageNotLoadedException(f'{self.url} did not open in {timeout} sec for {self.__class__.__name__}.\n'
                                     f'Current url is {self.driver.current_url}.')

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = TestsConfig.DEFAULT_WAITING_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout=timeout).until(ec.visibility_of_element_located(locator))

    def find_hidden(self, locator, timeout=None):
        return self.wait(timeout=timeout).until(ec.presence_of_element_located(locator))

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

    def write_into_input(self, input_locator, input_data):
        self.logger.debug(f"Writing data '{input_data}' into element with locator {input_locator}")
        input_element = self.find(input_locator)
        input_element.clear()
        input_element.send_keys(input_data)
