import os.path

import allure
import pytest
from _pytest.fixtures import FixtureRequest

from static.tests_config import TestsConfig
from ui.pages.campaings_page import CampaignsPage
from ui.pages.login_page import LoginPage


class BaseCase:

    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def failed_test_report(self, driver, request, test_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            screenshot_path = os.path.join(test_dir, TestsConfig.SCREENSHOT_NAME)
            driver.get_screenshot_as_file(screenshot_path)
            allure.attach.file(screenshot_path, TestsConfig.SCREENSHOT_NAME, attachment_type=allure.attachment_type.PNG)

            browser_log_path = os.path.join(test_dir, TestsConfig.BROWSER_LOG_FILE_NAME)
            with open(browser_log_path, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
            with open(browser_log_path, 'r') as f:
                allure.attach(f.read(), TestsConfig.BROWSER_LOG_FILE_NAME, attachment_type=allure.attachment_type.TEXT)

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, logger, request: FixtureRequest):
        self.driver = driver
        self.logger = logger
        self.login_page: LoginPage = request.getfixturevalue('login_page')

        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.campaigns_page: CampaignsPage = CampaignsPage(driver)
        self.logger.info("Initial setup completed")
