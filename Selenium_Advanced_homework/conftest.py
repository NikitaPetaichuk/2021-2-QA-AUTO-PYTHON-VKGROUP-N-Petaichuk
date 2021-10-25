import logging
import os.path
import shutil
import sys

import allure
import pytest
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager

from static.tests_config import TestsConfig
from ui.pages.login_page import LoginPage


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "UI: mark UI tests"
    )

    if sys.platform.startswith("win"):
        base_dir = "C:\\tests"
    else:
        base_dir = "/tmp/tests"

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)
    config.base_test_dir = base_dir


@pytest.fixture(scope='function')
def test_dir(request):
    test_dir = os.path.join(request.config.base_test_dir,
                            request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_'))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='session')
def repository_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='function')
def logger(test_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(test_dir, TestsConfig.INTERNAL_LOG_FILE_NAME)
    log_level = logging.DEBUG

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    logger = logging.getLogger('tests')
    logger.propagate = False
    logger.setLevel(log_level)
    logger.handlers.clear()
    logger.addHandler(file_handler)
    yield logger

    for handler in logger.handlers:
        handler.close()
    with open(log_file, 'r') as f:
        allure.attach(f.read(), TestsConfig.INTERNAL_LOG_FILE_NAME, attachment_type=allure.attachment_type.TEXT)


def get_driver():
    manager = ChromeDriverManager(version='latest', log_level=logging.CRITICAL)
    browser = Chrome(executable_path=manager.install())
    return browser


@pytest.fixture(scope='function')
def driver(test_dir):
    browser = get_driver()
    browser.get(TestsConfig.TEST_START_POINT_URL)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='session')
def cookies():
    driver = get_driver()
    driver.get(TestsConfig.TEST_START_POINT_URL)
    login_page = LoginPage(driver)
    login_page.login(TestsConfig.LOGIN_EMAIL, TestsConfig.LOGIN_PASSWORD)
    cookies = driver.get_cookies()
    driver.quit()
    return cookies


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver)
