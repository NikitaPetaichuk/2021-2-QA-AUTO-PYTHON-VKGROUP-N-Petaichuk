from static.tests_config import TestsConfig
from ui.locators.new_campaign_locators import NewCampaignLocators
from ui.pages.base_page import BasePage


class NewCampaignPage(BasePage):

    url = "https://target.my.com/campaign/new"
    locators = NewCampaignLocators()

    def create_new_campaign(self, picture_path, campaign_name):
        self.logger.info(f"Creating a new campaign with name {campaign_name}")
        self.click(self.locators.TRAFFIC_CONVERSION)
        self.write_into_input(self.locators.TARGETING_URL, TestsConfig.TARGET_URL)
        self.write_into_input(self.locators.CAMPAIGN_NAME_INPUT, campaign_name)
        self.click(self.locators.BANNER_PATTERN_CHOOSE)
        picture_input = self.find_hidden(self.locators.PICTURE_INPUT)
        picture_input.send_keys(picture_path)
        self.click(self.locators.SUBMIT_CAMPAIGN_BUTTON)
