from selenium.common.exceptions import TimeoutException

from ui.pages.base_page import BasePage
from ui.locators.campaigns_locators import CampaignsLocators
from ui.pages.new_campaign_page import NewCampaignPage
from ui.pages.segments_page import SegmentsPage


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
