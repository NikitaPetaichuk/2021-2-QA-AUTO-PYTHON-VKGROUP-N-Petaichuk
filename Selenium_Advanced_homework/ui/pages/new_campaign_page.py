from static.tests_config import TestsConfig
from ui.locators.new_campaign_locators import NewCampaignLocators
from ui.pages.base_page import BasePage
from utils.generate_funcs import generate_name


class NewCampaignPage(BasePage):

    url = "https://target.my.com/campaign/new"
    locators = NewCampaignLocators()

    def create_new_campaign(self, picture_path):
        campaign_name = generate_name("Campaign_to_Create")

        self.logger.info(f"Creating a new campaign with name {campaign_name}")
        self.click(self.locators.TRAFFIC_CONVERSION)
        target_url_input = self.find(self.locators.TARGETING_URL)
        target_url_input.send_keys(TestsConfig.TARGET_URL)
        campaign_name_input = self.find(self.locators.CAMPAIGN_NAME_INPUT)
        campaign_name_input.clear()
        campaign_name_input.send_keys(campaign_name)
        self.click(self.locators.BANNER_PATTERN_CHOOSE)
        picture_input = self.find_hidden(self.locators.PICTURE_INPUT)
        picture_input.send_keys(picture_path)
        self.click(self.locators.SUBMIT_CAMPAIGN_BUTTON)
        return campaign_name
