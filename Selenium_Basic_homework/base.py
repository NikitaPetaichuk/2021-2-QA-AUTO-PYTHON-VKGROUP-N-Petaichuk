import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.login_page import LoginPage
from ui.pages.logout_page import LogoutPage
from ui.pages.companies_page import CompaniesPage


class BaseCase:

    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, request: FixtureRequest):
        self.driver = driver
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.logout_page: LogoutPage = request.getfixturevalue('logout_page')
        self.companies_page: CompaniesPage = request.getfixturevalue('companies_page')
