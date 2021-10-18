import pytest
from selenium.webdriver import Chrome
from static.tests_config import TestsConfig
from static.urls_config import UrlsConfig
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.logout_page import LogoutPage
from ui.pages.campaigns_page import CampaignsPage
from ui.pages.navigation_page import NavigationPage
from ui.pages.profile_page import ProfilePage
from ui.pages.tools_page import ToolsPage


# Adding UI mark for tests
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "UI: mark UI tests"
    )


@pytest.fixture
def base_page(driver):
    return BasePage(driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def logout_page(driver):
    return LogoutPage(driver)


@pytest.fixture
def campaigns_page(driver):
    return CampaignsPage(driver)


@pytest.fixture
def navigation_page(driver):
    return NavigationPage(driver)


@pytest.fixture
def profile_page(driver):
    return ProfilePage(driver)


@pytest.fixture
def tools_page(driver):
    return ToolsPage(driver)


@pytest.fixture
def driver():
    browser = Chrome(executable_path=TestsConfig.DRIVER_PATH)
    browser.maximize_window()
    browser.get(UrlsConfig.MY_TARGET_SITE_URL)
    yield browser
    browser.close()
