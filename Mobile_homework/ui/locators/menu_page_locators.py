from appium.webdriver.common.mobileby import MobileBy


class MenuPageLocators:

    GO_TO_APP_INFO_PAGE = (MobileBy.ID, "ru.mail.search.electroscope:id/user_settings_about")
    GO_TO_NEWS_SOURCE_PAGE = (MobileBy.ID, "ru.mail.search.electroscope:id/user_settings_field_news_sources")
    GO_TO_SKILLS_PAGE = (MobileBy.ID, "ru.mail.search.electroscope:id/user_settings_skill_list")

    BACK_TO_MAIN_PAGE_BUTTON = (
        MobileBy.XPATH,
        '//android.widget.LinearLayout[@resource-id="ru.mail.search.electroscope:id/user_settings_toolbar"]/android'
        '.widget.ImageButton '
    )
