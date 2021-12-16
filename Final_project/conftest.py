import logging
import os
import shutil
import signal
import subprocess
import sys
import time

import allure
import pytest
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager

import static.config as conf
from api_clients.app_api_client import AppAPIClient
from static.links import Links
from static.tests_config import TestsConfig
from mysql.mysql_client import MysqlClient
from ui.pages.login_page import LoginPage
from utils.util_funcs import wait_app_ready


@pytest.fixture(scope='function', autouse=True)
def faker_seed():
    return int(time.time_ns())


def pytest_configure(config):
    if sys.platform.startswith("win"):
        base_dir = "C:\\tests"
    else:
        base_dir = "/tmp/tests"

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

        app_stdout_file_path = os.path.join(base_dir, TestsConfig.APP_STDOUT_FILE_NAME)
        app_stderr_file_path = os.path.join(base_dir, TestsConfig.APP_STDERR_FILE_NAME)
        app_stdout_file = open(app_stdout_file_path, "w")
        app_stderr_file = open(app_stderr_file_path, "w")

        app_process = subprocess.Popen(['docker-compose', 'up', '--force-recreate'],
                                       stdout=app_stdout_file, stderr=app_stderr_file)
        config.app_stdout_file = app_stdout_file
        config.app_stderr_file = app_stderr_file
        config.app_process = app_process

    wait_app_ready(Links.APP_API_STATUS, TestsConfig.APP_WAITING_TIMEOUT)

    mysql_client = MysqlClient(TestsConfig.MYSQL_USER, TestsConfig.MYSQL_PASSWORD, conf.MYSQL_DB)
    mysql_client.connect()

    config.base_test_dir = base_dir
    config.mysql_client = mysql_client


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        config.app_process.send_signal(signal.SIGINT)
        exit_code = config.app_process.wait()
        assert exit_code == 0

        down_return_code = subprocess.run(["docker-compose", "down"],
                                          stdout=config.app_stdout_file,
                                          stderr=config.app_stderr_file).returncode
        assert down_return_code == 0

        config.app_stdout_file.close()
        config.app_stderr_file.close()


@pytest.fixture(scope='function')
def test_dir(request):
    test_dir = os.path.join(request.config.base_test_dir,
                            request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_'))
    os.makedirs(test_dir)
    return test_dir


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
def mysql_client(request):
    client = request.config.mysql_client
    yield client
    client.connection.close()


def get_driver():
    manager = ChromeDriverManager(version='latest', log_level=logging.CRITICAL)
    browser = Chrome(executable_path=manager.install())
    return browser


@pytest.fixture(scope='function')
def driver(test_dir):
    browser = get_driver()
    browser.get(Links.APP_BASE_LINK)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver)
