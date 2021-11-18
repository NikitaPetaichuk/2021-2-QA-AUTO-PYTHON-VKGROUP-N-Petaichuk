import os

import allure
import pytest
from _pytest.fixtures import FixtureRequest

from static.tests_config import TestsConfig
from ui.pages.main_page import MainPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def failed_test_report(self, driver, request, test_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            screenshot_path = os.path.join(test_dir, TestsConfig.SCREENSHOT_NAME)
            driver.get_screenshot_as_file(screenshot_path)
            allure.attach.file(screenshot_path, TestsConfig.SCREENSHOT_NAME, attachment_type=allure.attachment_type.PNG)

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, logger, request: FixtureRequest):
        self.driver = driver
        self.logger = logger
        self.main_page: MainPage = request.getfixturevalue("main_page")

        self.logger.info("Initial setup completed")

    def go_to_page(self, page_name):
        menu_page = self.main_page.go_to_menu()
        return getattr(menu_page, f"go_to_{page_name}_page")()

    def return_to_main_page(self, now_page):
        back_to_menu_method = getattr(now_page, "back_to_menu", None)
        if back_to_menu_method is None:
            raise NotImplementedError(f"Page class {now_page.__class__.__name__} does not have 'back_to_menu' method")
        menu_page = back_to_menu_method()
        menu_page.back_to_main_page()
