import os

import allure
import pytest
from _pytest.fixtures import FixtureRequest

from api_clients.vk_api_client import VkAPIClient
from static.tests_config import TestsConfig
from ui.pages.login_page import LoginPage


class BaseCaseUI:

    authorize = False

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
    def setup(self, driver, mysql_client, user_builder, logger, request: FixtureRequest, faker):
        self.driver = driver
        self.logger = logger
        self.mysql_client = mysql_client
        self.vk_api_client = VkAPIClient(TestsConfig.VK_API_HOST, TestsConfig.VK_API_PORT)
        self.user_builder = user_builder
        self.login_page: LoginPage = request.getfixturevalue('login_page')

        if self.authorize:
            self.credentials, self.main_page = self.login_new_user(faker)
        self.logger.info("UI testing initial setup is completed")
        yield
        if self.authorize:
            self.mysql_client.delete_user(self.credentials["email"])
            self.vk_api_client.delete_vk_id(self.credentials["username"])

    @staticmethod
    def check_error_message(page, error_block_locator, message_to_check, equal=True):
        error_block = page.find(error_block_locator)
        if equal:
            assert error_block.text == message_to_check, f"Incorrect error message '{error_block.text}'"
        else:
            assert error_block.text != message_to_check, f"Incorrect error message '{error_block.text}'"

    def login_new_user(self, faker, vk_id=True):
        """
        User logging in:
        1. Generating sizes of user data.
        2. Generating user data, adding it to DB and (optionally) generating VK ID.
        3. Logging in using user data.
        """
        username_size = faker.pyint(min_value=6, max_value=16)
        email_prefix_size = faker.pyint(min_value=2, max_value=60)
        password_size = faker.pyint(min_value=6, max_value=255)

        user_data = self.user_builder.create_user_data(username_size, email_prefix_size, password_size)
        self.mysql_client.add_user(user_data)
        if vk_id:
            user_data["user_id"] = user_data["username"] + "_ID"
            self.vk_api_client.create_vk_id(user_data["username"], user_data["user_id"])

        main_page = self.login_page.login(user_data["username"], user_data["password"])
        return user_data, main_page
