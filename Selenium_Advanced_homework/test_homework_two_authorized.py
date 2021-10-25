import os

import allure
import pytest
from selenium.common.exceptions import TimeoutException

from base import BaseCase
from static.tests_config import TestsConfig
from utils.util_funcs import create_xpath_one_value_locator


class TestHomeworkTwoUnauthorized(BaseCase):

    @pytest.fixture(scope='function')
    def picture_path(self, repository_root):
        return os.path.join(repository_root, TestsConfig.PICTURE_DIRECTORY, TestsConfig.PICTURE_NAME)

    @allure.epic('QA Python Homework 2: Advanced UI testing')
    @allure.feature('MyTarget user functionality')
    @allure.story('Create a new campaign')
    @pytest.mark.UI
    def test_create_campaign(self, picture_path):
        with allure.step("Creating a campaign"):
            new_campaign_page = self.campaigns_page.go_to_new_campaign_page()
            campaign_name = new_campaign_page.create_new_campaign(picture_path)

        with allure.step("Checking the campaign creation"):
            campaign_locator = create_xpath_one_value_locator(
                self.campaigns_page.locators.CAMPAIGN_TABLE_CELL_TEMPLATE,
                campaign_name
            )
            campaign_cell = self.campaigns_page.find(campaign_locator)
            assert campaign_cell.is_displayed()

    @allure.epic('QA Python Homework 2: Advanced UI testing')
    @allure.feature('MyTarget user functionality')
    @allure.story('Create a new segment')
    @pytest.mark.UI
    def test_create_segment(self):
        with allure.step("Creating a segment"):
            segments_page = self.campaigns_page.go_to_segments_page()
            segment_name = segments_page.create_segment("Segment_to_Create")

        with allure.step("Checking the segment creation"):
            segment_locator = create_xpath_one_value_locator(
                segments_page.locators.SEGMENT_CELL_TEMPLATE,
                segment_name
            )
            segment_cell = segments_page.find(segment_locator)
            assert segment_cell.is_displayed()

    @allure.epic('QA Python Homework 2: Advanced UI testing')
    @allure.feature('MyTarget user functionality')
    @allure.story('Delete the existing segment')
    @pytest.mark.UI
    def test_delete_segment(self):
        with allure.step("Creating and deleting the segment"):
            segments_page = self.campaigns_page.go_to_segments_page()
            segment_name = segments_page.create_segment("Segment_to_Destroy")
            segments_page.delete_segment_by_name(segment_name)

        with allure.step("Checking the deleted segment not existing"):
            try:
                segments_page.find(segments_page.locators.SEGMENT_INSTRUCTION_TITLE, timeout=5)
            except TimeoutException:
                segments_page.find(segments_page.locators.SEGMENT_LIST_TITLE)
            segment_cell_locator = create_xpath_one_value_locator(
                segments_page.locators.SEGMENT_CELL_TEMPLATE,
                segment_name
            )
            assert not segments_page.is_element_exists(segment_cell_locator, timeout=5)
