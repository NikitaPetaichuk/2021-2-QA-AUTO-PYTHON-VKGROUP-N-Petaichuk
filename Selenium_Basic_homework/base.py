import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.logout_page import LogoutPage
from ui.pages.campaigns_page import CampaignsPage
from ui.pages.profile_page import ProfilePage


class BaseCase:

    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, request: FixtureRequest):
        self.driver = driver
        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.logout_page: LogoutPage = request.getfixturevalue('logout_page')
        self.campaigns_page: CampaignsPage = request.getfixturevalue('campaigns_page')
        self.profile_page: ProfilePage = request.getfixturevalue('profile_page')
