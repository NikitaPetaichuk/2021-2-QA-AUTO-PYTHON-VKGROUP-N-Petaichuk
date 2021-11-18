from selenium.common.exceptions import TimeoutException

from ui.locators.news_source_page_locators import NewsSourcePageLocators
from ui.pages.base_page import BasePage


class NewsSourcePage(BasePage):

    locators = NewsSourcePageLocators()

    def __init__(self, driver, menu_page):
        super().__init__(driver)
        self.menu_page = menu_page

    def set_news_source(self, news_source_title):
        news_source_locator = self.locators.get_news_source_title_locator(news_source_title)
        self.click(news_source_locator)
        return news_source_locator

    def check_news_source_selected(self, news_source_locator):
        locator_for_search = self.locators.get_news_source_checked_label(news_source_locator)
        try:
            self.find(locator_for_search)
            return True
        except TimeoutException:
            return False

    def back_to_menu(self):
        self.click(self.locators.BACK_BUTTON)
        return self.menu_page
