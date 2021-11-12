import allure
import pytest

from base import BaseCase
from static.tests_config import TestsConfig


class TestHomeworkFour(BaseCase):

    @allure.epic('QA Python Homework 4: Android testing')
    @allure.feature('Marussia functionality')
    @allure.story('Inputting command to Marussia')
    @pytest.mark.Android
    def test_input_command_to_marussia(self):
        with allure.step(f"Writing word '{TestsConfig.RUSSIA_INPUT_TEXT}' to Marussia"):
            self.main_page.send_command_to_marussia(TestsConfig.RUSSIA_INPUT_TEXT, first_one=True)

        with allure.step(f"Checking fact card got from Marussia about '{TestsConfig.RUSSIA_INPUT_TEXT}'"):
            fact_card_title = self.main_page.find_fact_card_title(TestsConfig.RUSSIA_FACT_CARD_TITLE)
            if fact_card_title is None:
                self.main_page.send_command_to_marussia(TestsConfig.RUSSIA_INPUT_TEXT)
                fact_card_title = self.main_page.find_fact_card_title(TestsConfig.RUSSIA_FACT_CARD_TITLE)
            assert fact_card_title is not None
            assert fact_card_title.text == TestsConfig.RUSSIA_FACT_CARD_TITLE

        with allure.step(f"Clicking on suggestion '{TestsConfig.RUSSIA_POPULATION_SUGGEST}'"):
            self.main_page.choose_suggestion(TestsConfig.RUSSIA_POPULATION_SUGGEST)

        with allure.step(f"Checking fact card on suggestion '{TestsConfig.RUSSIA_POPULATION_SUGGEST}'"):
            fact_card_title = self.main_page.find_fact_card_title(TestsConfig.RUSSIA_POPULATION_FACT_CARD_TITLE)
            assert fact_card_title is not None
            assert fact_card_title.text == TestsConfig.RUSSIA_POPULATION_FACT_CARD_TITLE

    @allure.epic('QA Python Homework 4: Android testing')
    @allure.feature('Marussia functionality')
    @allure.story('Inputting command to Marussia calculator')
    @pytest.mark.Android
    def test_input_command_to_marussia_calculator(self):
        with allure.step("Going to skills page"):
            menu_page = self.main_page.go_to_menu()
            skills_page = menu_page.go_to_skills_page()

        with allure.step(f"Choosing skill '{TestsConfig.CALCULATOR_SKILL_TITLE}'"):
            skills_page.choose_skill(TestsConfig.CALCULATOR_SKILL_TITLE)

        for index, command in enumerate(TestsConfig.COMMANDS):
            with allure.step(f"Sending command number {index + 1}: '{command}'"):
                self.main_page.send_command_to_marussia(command, first_one=(index == 0))
                command_result = str(eval(command))
                answer_message = self.main_page.find_message(command_result)
                assert answer_message is not None
                assert answer_message.text == command_result

    @allure.epic('QA Python Homework 4: Android testing')
    @allure.feature('Marussia functionality')
    @allure.story('Using news source')
    @pytest.mark.Android
    def test_news_source_usage(self):
        with allure.step("Going to news source page"):
            menu_page = self.main_page.go_to_menu()
            news_source_page = menu_page.go_to_news_source_page()

        with allure.step(f"Choosing news source '{TestsConfig.NEWS_SOURCE_TITLE}'"):
            news_source_locator = news_source_page.set_news_source(TestsConfig.NEWS_SOURCE_TITLE)

        with allure.step("Checking news source is selected"):
            assert news_source_page.check_news_source_selected(news_source_locator)

        with allure.step("Returning back to main page"):
            news_source_page.back_to_menu()
            menu_page.back_to_main_page()

        with allure.step(f"Sending command '{TestsConfig.NEWS_COMMAND}'"):
            self.main_page.send_command_to_marussia(TestsConfig.NEWS_COMMAND, first_one=True)

        with allure.step("Checking player track title"):
            player_track_title = self.main_page.find_player_track_title(TestsConfig.NEWS_PLAYER_TRACK_TITLE)
            assert player_track_title is not None
            assert player_track_title.text == TestsConfig.NEWS_PLAYER_TRACK_TITLE

    @allure.epic('QA Python Homework 4: Android testing')
    @allure.feature('Marussia functionality')
    @allure.story('Using app info page')
    @pytest.mark.Android
    def test_app_info_page_usage(self):
        with allure.step("Going to app info page"):
            menu_page = self.main_page.go_to_menu()
            app_info_page = menu_page.go_to_app_info_page()

        with allure.step("Checking app version"):
            version_label = app_info_page.find(app_info_page.locators.APP_VERSION_LABEL)
            assert version_label.text.endswith(TestsConfig.APK_VERSION)

        with allure.step("Checking copyright label"):
            copyright_label = app_info_page.find(app_info_page.locators.COPYRIGHT_LABEL)
            assert copyright_label.text == TestsConfig.EXPECTED_COPYRIGHT_LABEL
