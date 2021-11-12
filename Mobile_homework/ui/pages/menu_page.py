from ui.locators.menu_page_locators import MenuPageLocators
from ui.pages.app_info_page import AppInfoPage
from ui.pages.base_page import BasePage
from ui.pages.news_source_page import NewsSourcePage
from ui.pages.skills_page import SkillsPage


class MenuPage(BasePage):

    locators = MenuPageLocators()

    def go_to_app_info_page(self):
        self.swipe_to_element(self.locators.GO_TO_APP_INFO_PAGE)
        self.click(self.locators.GO_TO_APP_INFO_PAGE)
        return AppInfoPage(self.driver)

    def go_to_news_source_page(self):
        self.swipe_to_element(self.locators.GO_TO_NEWS_SOURCE_PAGE)
        self.click(self.locators.GO_TO_NEWS_SOURCE_PAGE)
        return NewsSourcePage(self.driver)

    def go_to_skills_page(self):
        self.swipe_to_element(self.locators.GO_TO_SKILLS_PAGE)
        self.click(self.locators.GO_TO_SKILLS_PAGE)
        return SkillsPage(self.driver)

    def back_to_main_page(self):
        self.click(self.locators.BACK_TO_MAIN_PAGE_BUTTON)
