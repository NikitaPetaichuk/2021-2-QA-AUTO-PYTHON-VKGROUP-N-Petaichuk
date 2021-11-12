from appium.webdriver.common.mobileby import MobileBy


class NewsSourcePageLocators:

    BACK_BUTTON = (
        MobileBy.XPATH,
        '//android.widget.LinearLayout['
        '@resource-id="ru.mail.search.electroscope:id/news_sources_toolbar"]/android'
        '.widget.ImageButton'
    )

    @staticmethod
    def get_news_source_title_locator(news_source_title_text):
        return (
            MobileBy.XPATH,
            '//android.widget.TextView[@resource-id = "ru.mail.search.electroscope:id/news_sources_item_title" and '
            f'contains(@text, "{news_source_title_text}")]'
        )

    @staticmethod
    def get_news_source_checked_label(news_source_locator):
        return (
            MobileBy.XPATH,
            f'{news_source_locator[1]}/following-sibling::'
            'android.widget.ImageView[@resource-id="ru.mail.search.electroscope:id/news_sources_item_selected"]'
        )
