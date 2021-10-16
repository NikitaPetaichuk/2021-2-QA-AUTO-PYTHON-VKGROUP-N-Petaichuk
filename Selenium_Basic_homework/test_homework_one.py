import pytest
from base import BaseCase


class TestHomeworkOne(BaseCase):

    @pytest.mark.UI
    def test_login(self):
        self.login_page.login()
        companies_page_title = self.companies_page.find(self.companies_page.locators.COMPANIES_PAGE_TITLE)
        assert companies_page_title.is_displayed()

    @pytest.mark.UI
    def test_logout(self):
        self.login_page.login()
        self.companies_page.find(self.companies_page.locators.COMPANIES_PAGE_TITLE)
        self.logout_page.logout()
        open_login_modal_button = self.login_page.find(self.login_page.locators.OPEN_LOGIN_MODAL_BUTTON)
        assert open_login_modal_button.is_displayed()

    def test_not_ui(self):
        assert 1 == 1
