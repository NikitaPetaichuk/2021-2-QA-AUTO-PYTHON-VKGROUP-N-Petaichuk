from ui.pages.base_page import BasePage
from ui.locators.campaigns_locators import CampaignsLocators
from ui.pages.new_campaign_page import NewCampaignPage
from ui.pages.segments_page import SegmentsPage


class CampaignsPage(BasePage):

    url = "https://target.my.com/dashboard"
    locators = CampaignsLocators()

    def go_to_new_campaign_page(self):
        if self.is_element_exists(self.locators.CREATE_CAMPAIGN_BUTTON):
            self.click(self.locators.CREATE_CAMPAIGN_BUTTON)
        else:
            self.click(self.locators.CREATE_CAMPAIGN_LINK)
        return NewCampaignPage(self.driver)

    def go_to_segments_page(self):
        self.click(self.locators.GO_TO_SEGMENTS_BUTTON)
        return SegmentsPage(self.driver)

    def delete_campaign_by_name(self, campaign_name):
        self.logger.info(f"Deleting the campaign with name {campaign_name}")
        campaign_row_id = self.get_id_by_campaign_name(campaign_name)
        campaign_checkbox_locator = self.locators.generate_campaign_checkbox_locator(campaign_row_id)
        self.click(campaign_checkbox_locator)
        self.click(self.locators.CAMPAIGN_CHOOSE_ACTION_SELECT)
        self.click(self.locators.DELETE_CAMPAIGNS_ACTION)
        self.find(self.locators.NOTIFY_SUCCESS_MESSAGE)

    def get_id_by_campaign_name(self, campaign_name):
        self.logger.info(f"Searching for id of campaign with name {campaign_name}")
        segment_locator = self.locators.generate_campaign_cell_locator(campaign_name)
        segment_cell = self.find(segment_locator)
        href = segment_cell.get_attribute('href')
        campaign_id = href.split("/")[-1].replace("?", "")
        self.logger.info(f"Got campaign id {campaign_id}")
        return campaign_id
