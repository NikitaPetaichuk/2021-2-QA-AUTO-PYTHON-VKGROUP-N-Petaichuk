import pytest
from base import BaseCase
from ui.locators.navigation_locators import NavigationLocators
from ui.locators.profile_locators import ProfileLocators
from ui.locators.tools_locators import ToolsLocators


FULL_NAME_TO_SET = "Test Account"
PHONE_NUMBER_TO_SET = "+7 (911) 111-22-33"


class TestHomeworkOne(BaseCase):

    @pytest.mark.UI
    def test_login(self):
        self.login_page.login()
        companies_page_title = self.campaigns_page.find(self.campaigns_page.locators.CAMPAIGNS_PAGE_TITLE)
        assert companies_page_title.is_displayed()
        self.logout_page.logout()

    @pytest.mark.UI
    def test_logout(self):
        self.login_page.login()
        self.campaigns_page.find(self.campaigns_page.locators.CAMPAIGNS_PAGE_TITLE)
        self.logout_page.logout()
        open_login_modal_button = self.login_page.find(self.login_page.locators.OPEN_LOGIN_MODAL_BUTTON)
        assert open_login_modal_button.is_displayed()

    @pytest.mark.UI
    def test_change_profile_data(self):
        self.login_page.login()
        self.navigation_page.click(self.navigation_page.locators.GO_TO_PROFILE_BUTTON)
        self.profile_page.change_profile_data(FULL_NAME_TO_SET, PHONE_NUMBER_TO_SET)
        submit_message = self.profile_page.find(self.profile_page.locators.SUBMIT_MESSAGE)
        assert submit_message.is_displayed()

        self.driver.refresh()
        full_name_input = self.profile_page.find(self.profile_page.locators.FULL_NAME_INPUT)
        phone_number_input = self.profile_page.find(self.profile_page.locators.PHONE_NUMBER_INPUT)
        assert full_name_input.get_attribute("value") == FULL_NAME_TO_SET
        assert phone_number_input.get_attribute("value") == PHONE_NUMBER_TO_SET
        self.logout_page.logout()

    @pytest.mark.UI
    @pytest.mark.parametrize(
        "destination_button_locator,transition_checker_locator",
        [
            pytest.param(NavigationLocators.GO_TO_PROFILE_BUTTON, ProfileLocators.PROFILE_TITLE),
            pytest.param(NavigationLocators.GO_TO_TOOLS_BUTTON, ToolsLocators.FEEDS_TITLE)
        ]
    )
    def test_go_to_page(self, destination_button_locator, transition_checker_locator):
        self.login_page.login()
        self.navigation_page.click(destination_button_locator)
        checker_element = self.base_page.find(transition_checker_locator)
        assert checker_element.is_displayed()
        self.logout_page.logout()
