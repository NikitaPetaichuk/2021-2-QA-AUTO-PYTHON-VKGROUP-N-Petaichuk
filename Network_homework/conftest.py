import logging
import os
import shutil
import sys

import allure
import pytest
from werkzeug.serving import WSGIRequestHandler

from mock_service.mock_app import app as mock_app
from static.tests_config import TestsConfig
from utils.thread_executor import FlaskThreadExecutor
from utils.util_funcs import wait_app_ready


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "Mock: mark Mock tests"
    )

    if sys.platform.startswith("win"):
        base_dir = "C:\\tests"
    else:
        base_dir = "/tmp/tests"

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

        mock_log_file_path = os.path.join(base_dir, TestsConfig.MOCK_LOG_FILE_NAME)
        WSGIRequestHandler.protocol_version = "HTTP/1.1"

        mock_executor = FlaskThreadExecutor(
            mock_app,
            TestsConfig.MOCK_HOST,
            TestsConfig.MOCK_PORT,
            mock_log_file_path
        )
        mock_executor.start()
        wait_app_ready(TestsConfig.MOCK_HOST, TestsConfig.MOCK_PORT, TestsConfig.WAIT_APP_TIME)

        config.mock_log_file_path = mock_log_file_path
        config.mock_executor = mock_executor
    config.base_test_dir = base_dir


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        config.mock_executor.stop()
        with open(config.mock_log_file_path, "r") as f:
            allure.attach(f.read(), TestsConfig.MOCK_LOG_FILE_NAME, attachment_type=allure.attachment_type.TEXT)


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

    logger = logging.getLogger(TestsConfig.TESTS_LOGS_NAME)
    logger.propagate = False
    logger.setLevel(log_level)
    logger.handlers.clear()
    logger.addHandler(file_handler)
    yield logger

    for handler in logger.handlers:
        handler.close()
    with open(log_file, 'r') as f:
        allure.attach(f.read(), TestsConfig.INTERNAL_LOG_FILE_NAME, attachment_type=allure.attachment_type.TEXT)
