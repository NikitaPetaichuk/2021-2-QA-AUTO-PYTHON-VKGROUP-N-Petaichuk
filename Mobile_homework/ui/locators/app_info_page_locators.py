from appium.webdriver.common.mobileby import MobileBy


class AppInfoPageLocators:

    APP_VERSION_LABEL = (MobileBy.ID, "ru.mail.search.electroscope:id/about_version")
    COPYRIGHT_LABEL = (MobileBy.ID, "ru.mail.search.electroscope:id/about_copyright")
