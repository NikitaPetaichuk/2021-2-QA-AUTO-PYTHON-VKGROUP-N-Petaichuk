import time
from static.tests_config import TestsConfig


def is_page_open(driver, url, timeout=TestsConfig.DEFAULT_TIMEOUT_FOR_PAGE_OPENING):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if driver.current_url == url:
            return True
    return False
