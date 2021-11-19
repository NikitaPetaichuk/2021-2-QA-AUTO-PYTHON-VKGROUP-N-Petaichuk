import logging
import os
import shutil
import sys

import allure
import pytest

from business_logic.nginx_log_parser import MysqlNginxLogParser
from mysql_client.mysql_client import MysqlClient
from static.tests_config import TestsConfig


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "Mysql: mark Mysql tests"
    )

    if sys.platform.startswith("win"):
        base_dir = "C:\\tests"
    else:
        base_dir = "/tmp/tests"

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    mysql_client = MysqlClient(TestsConfig.MYSQL_USER, TestsConfig.MYSQL_PASSWORD, TestsConfig.MYSQL_DB)
    if not hasattr(config, 'workerinput'):
        mysql_client.recreate_test_db()
    mysql_client.connect()
    if not hasattr(config, 'workerinput'):
        mysql_client.create_test_tables(TestsConfig.TABLES_NAMES)

    config.base_test_dir = base_dir
    config.mysql_client = mysql_client


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
def repository_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def access_log_path(repository_root):
    return os.path.join(repository_root, TestsConfig.ACCESS_LOG_DIRECTORY, TestsConfig.ACCESS_LOG_NAME)


@pytest.fixture(scope='session')
def mysql_client(request):
    client = request.config.mysql_client
    yield client
    client.connection.close()


@pytest.fixture(scope='session')
def nginx_log_parser(access_log_path):
    parser = MysqlNginxLogParser(
        access_log_path,
        TestsConfig.MYSQL_USER,
        TestsConfig.MYSQL_PASSWORD,
        TestsConfig.MYSQL_DB
    )
    yield parser
    parser.mysql_client.connection.close()
