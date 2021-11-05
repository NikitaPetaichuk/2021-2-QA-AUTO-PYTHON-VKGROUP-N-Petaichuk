import allure
import pytest
from selenium.common.exceptions import TimeoutException

from base import BaseCase


class TestHomeworkTwoUnauthorized(BaseCase):

    @allure.epic('QA Python Homework 2: Advanced UI testing')
    @allure.feature('MyTarget user functionality')
    @allure.story('Create a new campaign')
    @pytest.mark.UI
    def test_create_campaign(self, picture_path, faker):
        with allure.step("Creating a campaign"):
            new_campaign_page = self.campaigns_page.go_to_new_campaign_page()
            campaign_name = faker.unique.company()
            new_campaign_page.create_new_campaign(picture_path, campaign_name)

        with allure.step("Checking the campaign creation"):
            campaign_locator = self.campaigns_page.locators.generate_campaign_cell_locator(campaign_name)
            campaign_cell = self.campaigns_page.find(campaign_locator)
            assert campaign_cell.is_displayed()

        with allure.step("Tearing down test: deleting campaign"):
            self.campaigns_page.delete_campaign_by_name(campaign_name)

    @allure.epic('QA Python Homework 2: Advanced UI testing')
    @allure.feature('MyTarget user functionality')
    @allure.story('Create a new segment')
    @pytest.mark.UI
    def test_create_segment(self, faker):
        with allure.step("Creating a segment"):
            segments_page = self.campaigns_page.go_to_segments_page()
            segment_name = faker.unique.company() + " segment"
            segments_page.create_segment(segment_name)

        with allure.step("Checking the segment creation"):
            segment_locator = segments_page.locators.generate_segment_cell_locator(segment_name)
            segment_cell = segments_page.find(segment_locator)
            assert segment_cell.is_displayed()

        with allure.step("Tearing down test: deleting segment"):
            segments_page.delete_segment_by_name(segment_name)

    @allure.epic('QA Python Homework 2: Advanced UI testing')
    @allure.feature('MyTarget user functionality')
    @allure.story('Delete the existing segment')
    @pytest.mark.UI
    def test_delete_segment(self, faker):
        with allure.step("Creating the segment"):
            segments_page = self.campaigns_page.go_to_segments_page()
            segment_name = faker.unique.company() + " segment"
            segments_page.create_segment(segment_name)

        with allure.step("Deleting the segment"):
            segments_page.delete_segment_by_name(segment_name)

        with allure.step("Checking the deleted segment not existing"):
            try:
                instruction_title = segments_page.find(segments_page.locators.SEGMENT_INSTRUCTION_TITLE, timeout=5)
                assert instruction_title.is_displayed()
            except TimeoutException:
                segments_page.find(segments_page.locators.SEGMENT_LIST_TITLE)
                segment_cell_locator = segments_page.locators.generate_segment_cell_locator(segment_name)
                assert not segments_page.is_element_exists(segment_cell_locator, timeout=5)
