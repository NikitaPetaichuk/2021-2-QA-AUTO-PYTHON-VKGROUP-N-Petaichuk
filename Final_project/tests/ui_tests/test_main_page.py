from urllib.parse import urljoin

import pytest
import requests

from static.error_messages import ErrorMessages
from static.links import Links
from static.tests_config import TestsConfig
from tests.ui_tests.base_ui import BaseCaseUI
from ui.locators.main_page_locators import MainPageLocators
from ui.locators.not_found_locators import NOT_FOUND_LABEL


class TestLogin(BaseCaseUI):

    authorize = True

    def check_vk_id(self):
        vk_id = self.main_page.get_vk_id_value()
        assert vk_id == self.credentials["user_id"]

    def check_last_opened_tab_url(self, expected_url):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert self.driver.current_url == expected_url

    def test_user_name(self):
        username = self.main_page.get_user_name()

        assert self.credentials["username"] == username

    def test_logout(self):
        self.main_page.logout()

        assert self.driver.current_url == Links.APP_LOGIN_LINK

    def test_blocked_user(self):
        self.mysql_client.set_user_access(self.credentials["email"], 0)
        self.driver.refresh()

        error_block_locator = self.login_page.locators.ERROR_MESSAGE
        self.check_error_message(self.login_page, error_block_locator, ErrorMessages.MESSAGE_FOR_BLOCKED_USERS)

        self.login_page.login(self.credentials["username"], self.credentials["password"])

        self.check_error_message(self.login_page, error_block_locator, ErrorMessages.ACCOUNT_BLOCKED)

        self.mysql_client.set_user_access(self.credentials["email"], 1)
        self.login_page.login(self.credentials["username"], self.credentials["password"])

        assert self.driver.current_url == Links.APP_MAIN_PAGE

    def test_blocked_user_active_state(self):
        self.mysql_client.set_user_access(self.credentials["email"], 0)
        self.driver.refresh()

        user_entity = self.mysql_client.get_user("email", self.credentials["email"])
        assert user_entity.active == 0

    def test_get_vk_id(self):
        self.check_vk_id()

    def test_update_vk_id(self, faker):
        self.credentials["user_id"] = faker.pystr(min_chars=10, max_chars=20) + "_ID"
        self.vk_api_client.update_vk_id(self.credentials["username"], self.credentials["user_id"])
        self.driver.refresh()

        self.check_vk_id()

    def test_delete_vk_id(self):
        self.credentials["user_id"] = None
        self.vk_api_client.delete_vk_id(self.credentials["username"])
        self.driver.refresh()

        self.check_vk_id()

    def test_get_error_resource(self):
        response = requests.get(Links.APP_ERROR_RESOURCE)
        status_code = str(response.status_code)

        assert not (status_code.startswith("4") or status_code.startswith("5"))

    def test_get_non_existent_page(self, faker):
        error_path = faker.pystr(min_chars=15, max_chars=30)
        error_url = urljoin(Links.APP_BASE_LINK, error_path)
        self.driver.get(error_url)

        not_found_block = self.main_page.find(NOT_FOUND_LABEL)
        assert not_found_block.text == TestsConfig.NOT_FOUND_MESSAGE

    @pytest.mark.parametrize("click_on_logo", [True, False])
    def test_go_home(self, click_on_logo):
        self.main_page.go_home(click_on_logo)

        assert self.driver.current_url == Links.APP_MAIN_PAGE

    @pytest.mark.parametrize(
        "section_button,link_to_go,expected_url",
        [
            (MainPageLocators.PYTHON_BUTTON, None, Links.PYTHON_LINK),
            (MainPageLocators.PYTHON_BUTTON, Links.PYTHON_HISTORY_LINK, None),
            (MainPageLocators.PYTHON_BUTTON, Links.FLASK_LINK, None),
            (MainPageLocators.LINUX_BUTTON, None, Links.LINUX_LINK),
            (MainPageLocators.LINUX_BUTTON, Links.AKA_CENTOS_DOWNLOAD_LINK, Links.CENTOS_DOWNLOAD_LINK),
            (MainPageLocators.NETWORK_BUTTON, None, Links.NETWORK_LINK),
            (MainPageLocators.NETWORK_BUTTON, Links.WIRESHARK_NEWS_LINK, None),
            (MainPageLocators.NETWORK_BUTTON, Links.WIRESHARK_DOWNLOAD_LINK, None),
            (MainPageLocators.NETWORK_BUTTON, Links.TCPDUMP_EXAMPLES_LINK, None),
        ]
    )
    def test_go_from_sections(self, section_button, link_to_go, expected_url):
        self.main_page.go_from_section(section_button, link_to_go)

        url_for_check = link_to_go if expected_url is None else expected_url
        self.check_last_opened_tab_url(url_for_check)

    @pytest.mark.parametrize(
        "link_for_button,expected_url",
        [
            (Links.APP_API_PAPER_LINK, Links.API_PAPER_LINK),
            (Links.INTERNET_FUTURE_LINK, None),
            (Links.SMTP_PAPER_LINK, None),
        ]
    )
    def test_go_by_main_buttons(self, link_for_button, expected_url):
        self.main_page.go_by_main_button(link_for_button)

        url_for_check = link_for_button if expected_url is None else expected_url
        self.check_last_opened_tab_url(url_for_check)
