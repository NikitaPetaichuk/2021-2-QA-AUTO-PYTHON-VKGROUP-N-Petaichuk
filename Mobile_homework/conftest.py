import logging
import os.path
import shutil
import sys

import allure
import pytest
from appium import webdriver

from static.tests_config import TestsConfig
from ui.pages.main_page import MainPage


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "Android: mark Android tests"
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


@pytest.fixture(scope='session')
def apk_path(repository_root):
    return os.path.join(repository_root, TestsConfig.APK_INTERNAL_PATH, TestsConfig.APK_NAME)


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


@pytest.fixture(scope='session')
def capabilities(apk_path):
    return {
        "platformName": "Android",
        "platformVersion": "10.0",
        "deviceName": "Android Emulator",
        "app": apk_path,
        "appPackage": "ru.mail.search.electroscope",
        "appActivity": "ru.mail.search.electroscope.ui.activity.AssistantActivity",
        "autoGrantPermissions": True
    }


@pytest.fixture(scope='function')
def driver(capabilities):
    appium_browser = webdriver.Remote(TestsConfig.APPIUM_BASE_URL, desired_capabilities=capabilities)
    yield appium_browser
    appium_browser.quit()


@pytest.fixture(scope='function')
def main_page(driver):
    return MainPage(driver)
