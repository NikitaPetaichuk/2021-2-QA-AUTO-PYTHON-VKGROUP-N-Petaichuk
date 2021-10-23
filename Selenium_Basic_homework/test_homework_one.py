import pytest
from static.tests_config import TestsConfig
from static.urls_config import UrlsConfig
from base import BaseCase
from ui.locators.navigation_locators import NavigationLocators
from utils.util_funcs import is_page_open


class TestHomeworkOne(BaseCase):

    @pytest.mark.UI
    def test_login(self):
        self.login_page.login()
        assert is_page_open(self.driver, UrlsConfig.MY_TARGET_DASHBOARD_URL)

    @pytest.mark.UI
    def test_logout(self):
        self.login_page.login()
        self.campaigns_page.find(self.campaigns_page.locators.CAMPAIGNS_PAGE_TITLE)
        self.logout_page.logout()
        assert is_page_open(self.driver, UrlsConfig.MY_TARGET_SITE_URL)

    @pytest.mark.UI
    def test_change_profile_data(self):
        self.login_page.login()
        self.campaigns_page.click(NavigationLocators.GO_TO_PROFILE_BUTTON)
        self.profile_page.change_profile_data(TestsConfig.FULL_NAME_TO_SET, TestsConfig.PHONE_NUMBER_TO_SET)
        submit_message = self.profile_page.find(self.profile_page.locators.SUBMIT_MESSAGE)
        assert submit_message.is_displayed()

        self.driver.refresh()
        full_name_input = self.profile_page.find(self.profile_page.locators.FULL_NAME_INPUT)
        phone_number_input = self.profile_page.find(self.profile_page.locators.PHONE_NUMBER_INPUT)
        assert full_name_input.get_attribute("value") == TestsConfig.FULL_NAME_TO_SET
        assert phone_number_input.get_attribute("value") == TestsConfig.PHONE_NUMBER_TO_SET

    @pytest.mark.UI
    @pytest.mark.parametrize(
        "destination_button_locator,transition_url",
        [
            pytest.param(
                NavigationLocators.GO_TO_PROFILE_BUTTON,
                UrlsConfig.MY_TARGET_PROFILE_URL,
            ),
            pytest.param(
                NavigationLocators.GO_TO_TOOLS_BUTTON,
                UrlsConfig.MY_TARGET_TOOLS_FEEDS_URL,
            )
        ]
    )
    def test_go_to_page(self, destination_button_locator, transition_url):
        self.login_page.login()
        self.campaigns_page.click(destination_button_locator)
        assert is_page_open(self.driver, transition_url)
