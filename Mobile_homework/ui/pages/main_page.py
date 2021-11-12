from selenium.common.exceptions import TimeoutException, InvalidArgumentException

from static.tests_config import TestsConfig
from ui.locators.main_page_locators import MainPageLocators
from ui.pages.base_page import BasePage, UnreachableBySwipingException
from ui.pages.menu_page import MenuPage


class MainPage(BasePage):

    locators = MainPageLocators()

    def go_to_menu(self):
        self.click(self.locators.GO_TO_MENU_BUTTON)
        return MenuPage(self.driver)

    def send_command_to_marussia(self, command, first_one=False):
        if first_one:
            self.click(self.locators.KEYBOARD_BUTTON)
        else:
            self.click(self.locators.COMMAND_INPUT)
        self.write_into_input(self.locators.COMMAND_INPUT, command)
        self.click(self.locators.SEND_COMMAND)
        self.driver.hide_keyboard()

    def choose_suggestion(self, suggestion_text):
        locator_for_search = self.locators.get_suggestion_locator(suggestion_text)
        for _ in range(TestsConfig.MAX_SWIPES_COUNT):
            try:
                suggestion = self.find(locator_for_search)
                suggestion.click()
                return
            except TimeoutException:
                self.swipe_element_lo_left(self.locators.SUGGESTIONS_LIST)
        raise UnreachableBySwipingException(f"Suggestion '{suggestion_text}' can't be found")

    def find_fact_card_title(self, fact_card_title_text):
        locator_for_search = self.locators.get_fact_card_title_locator(fact_card_title_text)
        try:
            fact_card_title = self.find(locator_for_search)
            return fact_card_title
        except (TimeoutException, InvalidArgumentException):
            return None

    def find_message(self, message_text):
        locator_for_search = self.locators.get_message_locator(message_text)
        try:
            message = self.find(locator_for_search)
            return message
        except (TimeoutException, InvalidArgumentException):
            return None

    def find_player_track_title(self, player_track_title_text):
        locator_for_search = self.locators.get_player_track_title_locator(player_track_title_text)
        try:
            player_track_title = self.find(locator_for_search)
            return player_track_title
        except (TimeoutException, InvalidArgumentException):
            return None
