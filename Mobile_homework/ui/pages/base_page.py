import logging

import allure
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from static.tests_config import TestsConfig


class UnreachableBySwipingException(Exception):
    pass


class BasePage:

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.logger = logging.getLogger('tests')
        self.logger.info(f'Going to {self.__class__.__name__}')

    def wait(self, timeout=None):
        if timeout is None:
            timeout = TestsConfig.DEFAULT_WAITING_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout=timeout).until(ec.visibility_of_element_located(locator))

    @allure.step("Clicking on {locator}")
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

    def swipe_up(self, swipe_time=None):
        if swipe_time is None:
            swipe_time = TestsConfig.DEFAULT_SWIPE_TIME
        touch_action = TouchAction(self.driver)
        dimensions = self.driver.get_window_size()
        x = int(dimensions['width'] / 2)
        start_y = int(dimensions['height'] * 0.8)
        end_y = int(dimensions['height'] * 0.2)
        touch_action.press(x=x, y=start_y).wait(ms=swipe_time).move_to(x=x, y=end_y).release().perform()

    def swipe_to_element(self, locator):
        already_swiped = 0
        while len(self.driver.find_elements(*locator)) == 0:
            if already_swiped > TestsConfig.MAX_SWIPES_COUNT:
                raise UnreachableBySwipingException(
                    f"Element {locator} can't be found using {TestsConfig.MAX_SWIPES_COUNT} swipes."
                )
            self.swipe_up()
            already_swiped += 1

    def swipe_element_lo_left(self, locator):
        element = self.find(locator)
        print(element)
        left_x = element.location['x'] + 200
        right_x = left_x + element.rect['width'] - 400
        print(left_x, right_x)
        upper_y = element.location['y']
        lower_y = upper_y + element.rect['height']
        middle_y = (upper_y + lower_y) / 2
        print(upper_y, middle_y, lower_y)
        touch_action = TouchAction(self.driver)
        touch_action.press(x=right_x, y=middle_y).wait(ms=TestsConfig.DEFAULT_SWIPE_TIME)\
            .move_to(x=left_x, y=middle_y).release().perform()

    def write_into_input(self, input_locator, input_data):
        input_element = self.find(input_locator)
        input_element.clear()
        input_element.send_keys(input_data)
