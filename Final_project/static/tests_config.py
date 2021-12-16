class TestsConfig:

    APP_WAITING_TIMEOUT = 60
    DEFAULT_WAITING_TIMEOUT = 10
    CLICK_ATTEMPTS_COUNT = 3
    MAX_RESPONSE_LENGTH = 200

    MYSQL_USER = 'test_qa'
    MYSQL_PASSWORD = 'qa_test'
    VK_API_HOST = '127.0.0.1'
    VK_API_PORT = '9090'
    INTERNAL_LOG_FILE_NAME = 'tests.log'
    SCREENSHOT_NAME = 'failure_state.png'
    BROWSER_LOG_FILE_NAME = 'browser.log'
    APP_STDOUT_FILE_NAME = 'app_stdout.txt'
    APP_STDERR_FILE_NAME = 'app_stderr.txt'

    DANGER_MESSAGE_STYLE = "uk-alert-danger"
    NOT_FOUND_MESSAGE = "Page Not Found"
