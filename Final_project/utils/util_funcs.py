import time

import requests
from requests.exceptions import ConnectionError


class AppNotStartedError(Exception):
    pass


def wait_app_ready(status_url, wait_time):
    started = False
    start_time = time.time()
    while time.time() - start_time <= wait_time:
        try:
            response = requests.get(status_url)
            if response.json()["status"] == "ok":
                started = True
                break
            else:
                continue
        except ConnectionError:
            pass
    if not started:
        raise AppNotStartedError(
            f"Status request by url '{status_url}' didn't give positive response in {wait_time} s."
        )
