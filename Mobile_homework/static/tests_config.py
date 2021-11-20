import re


class TestsConfig:

    APPIUM_BASE_URL = "http://127.0.0.1:4723/wd/hub"
    CLICK_ATTEMPTS_COUNT = 3
    DEFAULT_WAITING_TIMEOUT = 10
    MAX_SWIPES_COUNT = 5
    DEFAULT_SWIPE_TIME = 200
    INTERNAL_LOG_FILE_NAME = "tests.log"
    SCREENSHOT_NAME = "failed_state.png"

    APK_INTERNAL_PATH = "apk"
    APK_NAME = "Marussia_v1.50.2.apk"

    RUSSIA_INPUT_TEXT = "Russia"
    RUSSIA_FACT_CARD_TITLE = "Россия"
    RUSSIA_POPULATION_SUGGEST = "население россии"
    RUSSIA_POPULATION_FACT_CARD_TITLE = "146 млн."

    CALCULATOR_SKILL_TITLE = "Калькулятор"
    COMMANDS = ["150 + 150", "70 - 1"]

    NEWS_SOURCE_TITLE = "Вести FM"
    NEWS_COMMAND = "News"
    NEWS_PLAYER_TRACK_TITLE = "Вести ФМ"

    EXPECTED_COPYRIGHT_LABEL = "Mail.ru Group © 1998–2021. Все права защищены."

    @classmethod
    def apk_version(cls):
        version_regex = r"v(\d\.\d\d\.\d)"
        return re.search(version_regex, cls.APK_NAME).group(1)
