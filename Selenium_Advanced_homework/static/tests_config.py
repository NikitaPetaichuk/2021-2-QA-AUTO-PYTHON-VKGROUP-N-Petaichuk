class TestsConfig:

    TEST_START_POINT_URL = 'https://target.my.com/'

    CLICK_ATTEMPTS_COUNT = 3
    DEFAULT_WAITING_TIMEOUT = 10
    SCREENSHOT_NAME = 'failure_state.png'
    BROWSER_LOG_FILE_NAME = 'browser.log'
    INTERNAL_LOG_FILE_NAME = 'tests.log'
    PICTURE_DIRECTORY = 'static'
    PICTURE_NAME = 'banner.jpg'
    INVALID_LOGIN_MESSAGE = 'Invalid login or password'
    AUTH_COOKIES_NAMES_LIST = [
        'ssdc', 'csrftoken', 'tmr_detect', 'sdc', 'mc', 'mrcu'
    ]

    LOGIN_EMAIL = 'pet.ai.4.uk@yandex.ru'
    LOGIN_PASSWORD = 'TestAccount123'
    TARGET_URL = 'mail.ru'

