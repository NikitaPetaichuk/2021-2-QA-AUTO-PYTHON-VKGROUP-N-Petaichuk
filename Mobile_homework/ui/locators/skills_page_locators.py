from appium.webdriver.common.mobileby import MobileBy


class SkillsPageLocators:

    @staticmethod
    def get_skill_title_locator(skill_title_text):
        return (
            MobileBy.XPATH,
            '//android.widget.TextView[@resource-id = "ru.mail.search.electroscope:id/item_skill_list_title" and '
            f'contains(@text, "{skill_title_text}")] '
        )
