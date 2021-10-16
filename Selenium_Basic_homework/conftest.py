import pytest
from selenium.webdriver import Chrome
from ui.pages.login_page import LoginPage
from ui.pages.logout_page import LogoutPage
from ui.pages.companies_page import CompaniesPage


DRIVER_PATH = '/home/mrpedro/drivers/chromedriver'
MY_TARGET_SITE_URL = 'https://target.my.com/'


# Adding UI mark for tests
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "UI: mark UI tests"
    )


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def logout_page(driver):
    return LogoutPage(driver)


@pytest.fixture
def companies_page(driver):
    return CompaniesPage(driver)


@pytest.fixture
def driver():
    browser = Chrome(executable_path=DRIVER_PATH)
    browser.maximize_window()
    browser.get(MY_TARGET_SITE_URL)
    yield browser
    browser.close()
