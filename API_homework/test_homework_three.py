import allure
import pytest

from base import ApiBaseCase


class TestHomeworkThree(ApiBaseCase):

    @allure.epic('QA Python Homework 3: API testing')
    @allure.feature('MyTarget API functionality')
    @allure.story('Create a new campaign (Traffic, Banner)')
    @pytest.mark.API
    def test_create_traffic_banner_campaign(self, faker, picture_path):
        with allure.step("Creating a new campaign"):
            campaign_name = faker.unique.company() + " campaign"
            created_campaign = self.api_client.post_create_traffic_banner_campaign(campaign_name, picture_path)

        with allure.step("Check the new campaign creation"):
            campaign_id = created_campaign["id"]
            campaigns_list = self.api_client.get_campaigns()
            found_campaign = next((campaign for campaign in campaigns_list if campaign["id"] == campaign_id), None)
            assert found_campaign is not None

        with allure.step("Tearing down: deleting the created campaign"):
            self.api_client.post_delete_campaign(campaign_id)

    @allure.epic('QA Python Homework 3: API testing')
    @allure.feature('MyTarget API functionality')
    @allure.story('Create a new segment')
    @pytest.mark.API
    def test_create_segment(self, faker):
        with allure.step("Creating a new segment"):
            segment_name = faker.unique.company() + " segment"
            segment = self.api_client.post_create_segment(segment_name)
            assert segment['name'] == segment_name

        with allure.step("Checking the segment existence"):
            segment_id = segment['id']
            segment_object = self.api_client.get_segment(segment_id)
            assert segment_object is not None
            assert segment_object["id"] == segment_id

        with allure.step("Tearing down: delete the created segment"):
            self.api_client.post_delete_segment(segment_id)

    @allure.epic('QA Python Homework 3: API testing')
    @allure.feature('MyTarget API functionality')
    @allure.story('Delete the segment')
    @pytest.mark.API
    def test_delete_segment(self, faker):
        with allure.step("Setting up: creating a new segment"):
            segment_name = faker.unique.company() + " segment (to delete)"
            segment = self.api_client.post_create_segment(segment_name)

        with allure.step("Deleting the created segment"):
            segment_id = segment['id']
            delete_response = self.api_client.post_delete_segment(segment_id)
            assert len(delete_response["errors"]) == 0
            assert delete_response["successes"][0]["source_id"] == segment_id
