from ui.pages.base_page import BasePage
from ui.locators.segments_locators import SegmentsLocators
from utils.generate_funcs import generate_name
from utils.util_funcs import create_xpath_one_value_locator


class SegmentsPage(BasePage):

    url = "https://target.my.com/segments/segments_list"
    locators = SegmentsLocators()

    def create_segment(self, segment_prefix):
        segment_name = generate_name(segment_prefix)

        self.logger.info(f"Creating a new segment with name {segment_name}")
        if self.is_element_exists(self.locators.CREATE_SEGMENT_BUTTON):
            self.click(self.locators.CREATE_SEGMENT_BUTTON)
        else:
            self.click(self.locators.CREATE_SEGMENT_LINK)
        self.click(self.locators.ADDING_SEGMENT_CHECKBOX)
        self.click(self.locators.ADDING_SEGMENT_SUBMIT)
        segment_name_input = self.find(self.locators.SEGMENT_NAME_INPUT)
        segment_name_input.clear()
        segment_name_input.send_keys(segment_name)
        self.click(self.locators.SUBMIT_SEGMENT_BUTTON)
        return segment_name

    def delete_segment_by_name(self, segment_name):
        self.logger.info(f"Deleting the segment with name {segment_name}")
        segment_row_id = self.get_id_by_segment_name(segment_name)
        segment_checkbox_locator = create_xpath_one_value_locator(
            self.locators.SEGMENT_CHOOSE_CHECKBOX_TEMPLATE,
            segment_row_id
        )
        self.click(segment_checkbox_locator)
        self.click(self.locators.SEGMENTS_CHOOSE_ACTION_SELECT)
        self.click(self.locators.DELETE_SEGMENTS_ACTION)

    def get_id_by_segment_name(self, segment_name):
        self.logger.info(f"Searching for id of segment with name {segment_name}")
        segment_locator = create_xpath_one_value_locator(
            self.locators.SEGMENT_CELL_TEMPLATE,
            segment_name
        )
        segment_cell = self.find(segment_locator)
        href = segment_cell.get_attribute('href')
        return href.split("/")[-1]
