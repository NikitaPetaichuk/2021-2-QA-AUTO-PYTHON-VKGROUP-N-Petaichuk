from urllib.parse import urljoin

import allure
import pytest
import requests

from static.error_messages import ErrorMessages
from static.links import Links
from static.tests_config import TestsConfig
from tests.ui_tests.base_ui import BaseCaseUI
from ui.locators.main_page_locators import MainPageLocators
from ui.locators.not_found_locators import NOT_FOUND_LABEL


class TestMainPage(BaseCaseUI):

    authorize = True

    def check_vk_id(self):
        vk_id = self.main_page.get_vk_id_value()
        assert vk_id == self.credentials["user_id"], "Incorrect VK ID"

    def check_last_opened_tab_url(self, expected_url):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert self.driver.current_url == expected_url, f"Incorrect current url " \
                                                        f"'{self.driver.current_url}'"

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App main page functionality')
    @allure.story('Checking username on main page')
    def test_user_name(self):
        """
        Test for checking username on main page.
        Steps:
        1. Getting username from main page.
        2. Checking username.
        Expected result:
        Username is correct.
        """
        with allure.step('Getting username from main page'):
            username = self.main_page.get_user_name()

        with allure.step('Checking username'):
            assert self.credentials["username"] == username, "Incorrect displayed username"

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App main page functionality')
    @allure.story('Checking logging out from main page')
    def test_logout(self):
        """
        Test for checking username on main page.
        Steps:
        1. Logging out.
        2. Checking current url and active state.
        Expected result:
        User is logged out (active state is 0, current url is login url).
        """
        with allure.step('Logging out'):
            self.main_page.logout()

        with allure.step('Checking current url and active state'):
            assert self.driver.current_url == Links.APP_LOGIN_LINK, f"Incorrect current url " \
                                                                    f"'{self.driver.current_url}'"
            user_entity = self.mysql_client.get_user("email", self.credentials["email"])
            assert user_entity.active == 0, "Incorrect active state"

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App main page functionality')
    @allure.story('Checking user access to main page in different states')
    def test_user_access_to_main_page(self):
        """
        Test for checking user access to main page in different states.
        Steps:
        1. Setting access state to 0 and refreshing page.
        2. Checking current url and error message.
        3. Trying to log in.
        4. Checking current url and error message and log in try.
        5. Setting access state to 1 and trying to log in again.
        6. Checking current url.
        Expected result:
        User doesn't have access to main page while access state is 0.
        User is given access to main page when access state becomes 1.
        """
        with allure.step('Setting access state to 0 and refreshing page'):
            self.mysql_client.set_user_access(self.credentials["email"], 0)
            self.driver.refresh()

        with allure.step('Checking current url and error message'):
            assert self.driver.current_url.startswith(Links.APP_LOGIN_LINK), f"Incorrect current url " \
                                                                             f"'{self.driver.current_url}'"
            error_block_locator = self.login_page.locators.ERROR_MESSAGE
            self.check_error_message(self.login_page, error_block_locator, ErrorMessages.MESSAGE_FOR_BLOCKED_USERS)

        with allure.step('Trying to log in'):
            self.login_page.login(self.credentials["username"], self.credentials["password"])

        with allure.step('Checking current url and error message and log in try'):
            assert self.driver.current_url.startswith(Links.APP_LOGIN_LINK), f"Incorrect current url " \
                                                                             f"'{self.driver.current_url}'"
            self.check_error_message(self.login_page, error_block_locator, ErrorMessages.ACCOUNT_BLOCKED)

        with allure.step('Setting access state to 1 and trying to log in again'):
            self.mysql_client.set_user_access(self.credentials["email"], 1)
            self.login_page.login(self.credentials["username"], self.credentials["password"])

        with allure.step('Checking current url'):
            assert self.driver.current_url == Links.APP_MAIN_PAGE, f"Incorrect current url " \
                                                                   f"'{self.driver.current_url}'"

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App main page functionality')
    @allure.story('Checking blocked user active state')
    def test_blocked_user_active_state(self):
        """
        Test for checking blocked user active state.
        Steps:
        1. Setting access state to 0 and refreshing page.
        2. Checking user active state.
        Expected result:
        User active state is 0 (he doesn't have access to main page).
        """
        with allure.step('Setting access state to 0 and refreshing page'):
            self.mysql_client.set_user_access(self.credentials["email"], 0)
            self.driver.refresh()

        with allure.step('Checking user active state'):
            user_entity = self.mysql_client.get_user("email", self.credentials["email"])
            assert user_entity.active == 0, "Incorrect active state"

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App main page functionality')
    @allure.story('Checking user VK ID')
    def test_get_vk_id(self):
        """
        Test for checking user VK ID.
        Steps:
        1. Getting and checking user VK ID.
        Expected result:
        User VK ID is correct.
        """
        with allure.step('Getting and checking user VK ID'):
            self.check_vk_id()

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App main page functionality')
    @allure.story('Checking user VK ID after updating')
    def test_update_vk_id(self):
        """
        Test for checking user VK ID after updating.
        Steps:
        1. Updating VK ID and refreshing page.
        2. Getting and checking user VK ID.
        Expected result:
        User VK ID is correct.
        """
        with allure.step('Updating VK ID and refreshing page'):
            self.credentials["user_id"] = self.user_builder.create_user_data_string(20, 10) + "_ID"
            self.vk_api_client.update_vk_id(self.credentials["username"], self.credentials["user_id"])
            self.driver.refresh()

        with allure.step('Getting and checking user VK ID'):
            self.check_vk_id()

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App main page functionality')
    @allure.story('Checking user VK ID after deleting')
    def test_delete_vk_id(self):
        """
        Test for checking user VK ID after deleting.
        Steps:
        1. Deleting VK ID and refreshing page.
        2. Getting and checking user VK ID.
        Expected result:
        User VK ID is correct.
        """
        with allure.step('Deleting VK ID and refreshing page'):
            self.credentials["user_id"] = None
            self.vk_api_client.delete_vk_id(self.credentials["username"])
            self.driver.refresh()

        with allure.step('Getting and checking user VK ID'):
            self.check_vk_id()

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App main page functionality')
    @allure.story('Checking possibly error resource loading')
    def test_get_error_resource(self):
        """
        Test for checking possible error resource loading.
        Steps:
        1. Getting possibly error resource.
        2. Checking status code.
        Expected result:
        Resource is loaded.
        """
        with allure.step('Getting possibly error resource'):
            response = requests.get(Links.APP_ERROR_RESOURCE)

        with allure.step('Checking status code'):
            status_code = str(response.status_code)
            assert not (status_code.startswith("4") or status_code.startswith("5")), "Incorrect response status code"

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App main page functionality')
    @allure.story('Checking 404 status for non-existent page')
    def test_get_non_existent_page(self):
        """
        Test for checking 404 status for non-existent page.
        Steps:
        1. Creating url for non-existent page.
        2. Going to non-existent page.
        2. Checking Not Found message.
        Expected result:
        Not Found message is correct.
        """
        with allure.step('Creating url for non-existent page'):
            error_path = self.user_builder.create_user_data_string(30, 15)
            error_url = urljoin(Links.APP_SELENOID_BASE_LINK, error_path)

        with allure.step('Going to non-existent page'):
            self.driver.get(error_url)

        with allure.step('Checking Not Found message'):
            not_found_block = self.main_page.find(NOT_FOUND_LABEL)
            assert not_found_block.text == TestsConfig.NOT_FOUND_MESSAGE, "Incorrect Not Found message"

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App main page functionality')
    @allure.story('Checking going to main page by buttons')
    @pytest.mark.parametrize("click_on_logo", [True, False])
    def test_go_home(self, click_on_logo):
        """
        Test for checking going to main page by buttons.
        Steps:
        1. Going to main page by selected button.
        2. Checking current url.
        Expected result:
        Current url is main page url.
        """
        with allure.step('Checking Not Found message'):
            self.main_page.go_home(click_on_logo)

        with allure.step('Checking Not Found message'):
            assert self.driver.current_url == Links.APP_MAIN_PAGE, f"Incorrect current url " \
                                                                   f"'{self.driver.current_url}'"

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App main page functionality')
    @allure.story('Checking going to different pages by NavBar buttons')
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
        """
        Test for checking going to different pages by NavBar buttons.
        Steps:
        1. Going to page by selected NavBar button.
        2. Checking last opened tab current url.
        Expected result:
        Current url of last opened tab is equal to expected url.
        """
        with allure.step('Going to page by selected NavBar button'):
            self.main_page.go_from_section(section_button, link_to_go)

        with allure.step('Checking current url'):
            url_for_check = link_to_go if expected_url is None else expected_url
            self.check_last_opened_tab_url(url_for_check)

    @allure.epic('QA Python Final project: UI testing')
    @allure.feature('App main page functionality')
    @allure.story('Checking going to different pages by main buttons')
    @pytest.mark.parametrize(
        "link_for_button,expected_url",
        [
            (Links.APP_API_PAPER_LINK, Links.API_PAPER_LINK),
            (Links.INTERNET_FUTURE_LINK, None),
            (Links.SMTP_PAPER_LINK, None),
        ]
    )
    def test_go_by_main_buttons(self, link_for_button, expected_url):
        """
        Test for checking going to different pages by main buttons.
        Steps:
        1. Going to page by selected main button.
        2. Checking last opened tab current url.
        Expected result:
        Current url of last opened tab is equal to expected url.
        """
        with allure.step('Going to page by selected main button'):
            self.main_page.go_by_main_button(link_for_button)

        with allure.step('Checking last opened tab current url'):
            url_for_check = link_for_button if expected_url is None else expected_url
            self.check_last_opened_tab_url(url_for_check)
