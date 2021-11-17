import allure
import pytest

from base import BaseCase
from static.tests_config import TestsConfig


class TestHomeworkFour(BaseCase):

    def check_answer_post_existence(self, title, find_title_method, resend_command=False, command=''):
        post_title = find_title_method(title)
        if post_title is None and resend_command:
            self.main_page.send_command_to_marussia(command)
            post_title = self.main_page.find_fact_card_title(title)
        assert post_title is not None
        assert post_title.text == title

    def check_calculator_command_execution(self, command, command_index):
        self.main_page.send_command_to_marussia(command, first_one=(command_index == 0))
        command_result = str(eval(command))
        answer_message = self.main_page.find_message(command_result)
        assert answer_message is not None
        assert answer_message.text == command_result

    @allure.epic('QA Python Homework 4: Android testing')
    @allure.feature('Marussia functionality')
    @allure.story('Inputting command to Marussia')
    @pytest.mark.Android
    def test_input_command_to_marussia(self):
        with allure.step(f"Writing word '{TestsConfig.RUSSIA_INPUT_TEXT}' to Marussia"):
            self.main_page.send_command_to_marussia(TestsConfig.RUSSIA_INPUT_TEXT, first_one=True)

        with allure.step(f"Checking fact card got from Marussia about '{TestsConfig.RUSSIA_INPUT_TEXT}'"):
            self.check_answer_post_existence(
                TestsConfig.RUSSIA_FACT_CARD_TITLE,
                self.main_page.find_fact_card_title,
                resend_command=True,
                command=TestsConfig.RUSSIA_INPUT_TEXT
            )

        with allure.step(f"Clicking on suggestion '{TestsConfig.RUSSIA_POPULATION_SUGGEST}'"):
            self.main_page.choose_suggestion(TestsConfig.RUSSIA_POPULATION_SUGGEST)

        with allure.step(f"Checking fact card on suggestion '{TestsConfig.RUSSIA_POPULATION_SUGGEST}'"):
            self.check_answer_post_existence(
                TestsConfig.RUSSIA_POPULATION_FACT_CARD_TITLE,
                self.main_page.find_fact_card_title
            )

    @allure.epic('QA Python Homework 4: Android testing')
    @allure.feature('Marussia functionality')
    @allure.story('Inputting command to Marussia calculator')
    @pytest.mark.Android
    def test_input_command_to_marussia_calculator(self):
        with allure.step("Going to skills page"):
            skills_page = self.go_to_page("skills")

        with allure.step(f"Choosing skill '{TestsConfig.CALCULATOR_SKILL_TITLE}'"):
            skills_page.choose_skill(TestsConfig.CALCULATOR_SKILL_TITLE)

        for index, command in enumerate(TestsConfig.COMMANDS):
            with allure.step(f"Sending command number {index + 1}: '{command}'"):
                self.check_calculator_command_execution(command, index)

    @allure.epic('QA Python Homework 4: Android testing')
    @allure.feature('Marussia functionality')
    @allure.story('Using news source')
    @pytest.mark.Android
    def test_news_source_usage(self):
        with allure.step("Going to news source page"):
            news_source_page = self.go_to_page("news_source")

        with allure.step(f"Choosing news source '{TestsConfig.NEWS_SOURCE_TITLE}'"):
            news_source_locator = news_source_page.set_news_source(TestsConfig.NEWS_SOURCE_TITLE)

        with allure.step("Checking news source is selected"):
            assert news_source_page.check_news_source_selected(news_source_locator)

        with allure.step("Returning back to main page"):
            self.return_to_main_page(news_source_page)

        with allure.step(f"Sending command '{TestsConfig.NEWS_COMMAND}'"):
            self.main_page.send_command_to_marussia(TestsConfig.NEWS_COMMAND, first_one=True)

        with allure.step("Checking player track title"):
            self.check_answer_post_existence(
                TestsConfig.NEWS_PLAYER_TRACK_TITLE,
                self.main_page.find_player_track_title
            )

    @allure.epic('QA Python Homework 4: Android testing')
    @allure.feature('Marussia functionality')
    @allure.story('Using app info page')
    @pytest.mark.Android
    def test_app_info_page_usage(self):
        with allure.step("Going to app info page"):
            app_info_page = self.go_to_page("app_info")

        with allure.step("Checking app version"):
            version_label = app_info_page.find(app_info_page.locators.APP_VERSION_LABEL)
            assert version_label.text.endswith(TestsConfig.apk_version())

        with allure.step("Checking copyright label"):
            copyright_label = app_info_page.find(app_info_page.locators.COPYRIGHT_LABEL)
            assert copyright_label.text == TestsConfig.EXPECTED_COPYRIGHT_LABEL
