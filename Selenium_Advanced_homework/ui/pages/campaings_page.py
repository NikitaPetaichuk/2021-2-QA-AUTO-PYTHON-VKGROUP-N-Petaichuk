from ui.pages.base_page import BasePage
from ui.locators.campaigns_locators import CampaignsLocators
from ui.pages.new_campaign_page import NewCampaignPage
from ui.pages.segments_page import SegmentsPage
from utils.util_funcs import create_xpath_one_value_locator


class CampaignsPage(BasePage):

    url = "https://target.my.com/dashboard"
    locators = CampaignsLocators()

    def go_to_new_campaign_page(self):
        self.logger.info("Going to new campaign page")
        if self.is_element_exists(self.locators.CREATE_CAMPAIGN_BUTTON):
            self.click(self.locators.CREATE_CAMPAIGN_BUTTON)
        else:
            self.click(self.locators.CREATE_CAMPAIGN_LINK)
        return NewCampaignPage(self.driver)

    def go_to_segments_page(self):
        self.logger.info("Going to segments page")
        self.click(self.locators.GO_TO_SEGMENTS_BUTTON)
        return SegmentsPage(self.driver)

    def delete_campaign_by_name(self, campaign_name):
        self.logger.info(f"Deleting the campaign with name {campaign_name}")
        campaign_row_id = self.get_id_by_campaign_name(campaign_name)
        print(campaign_row_id)
        campaign_checkbox_locator = create_xpath_one_value_locator(
            self.locators.CAMPAIGN_CHOOSE_CHECKBOX_TEMPLATE,
            campaign_row_id
        )
        self.click(campaign_checkbox_locator)
        self.click(self.locators.CAMPAIGN_CHOOSE_ACTION_SELECT)
        self.click(self.locators.DELETE_CAMPAIGNS_ACTION)

    def get_id_by_campaign_name(self, campaign_name):
        self.logger.info(f"Searching for id of campaign with name {campaign_name}")
        segment_locator = create_xpath_one_value_locator(
            self.locators.CAMPAIGN_TABLE_CELL_TEMPLATE,
            campaign_name
        )
        segment_cell = self.find(segment_locator)
        href = segment_cell.get_attribute('href')
        return href.split("/")[-1].replace("?", "")
