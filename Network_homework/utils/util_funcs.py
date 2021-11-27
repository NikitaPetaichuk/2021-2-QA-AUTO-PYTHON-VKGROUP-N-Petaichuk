import time

import requests
from requests.exceptions import ConnectionError


class AppNotStartedError(Exception):
    pass


def wait_app_ready(app_host, app_port, wait_time):
    started = False
    start_time = time.time()
    while time.time() - start_time <= wait_time:
        try:
            requests.get(f'http://{app_host}:{app_port}')
            started = True
            break
        except ConnectionError:
            pass
    if not started:
        raise AppNotStartedError(f"App '{app_host}:{app_port}' wasn't started in {wait_time} s.")


def generate_non_existing_key(keys_list):
    return max(keys_list) + 1 if len(keys_list) != 0 else 0
