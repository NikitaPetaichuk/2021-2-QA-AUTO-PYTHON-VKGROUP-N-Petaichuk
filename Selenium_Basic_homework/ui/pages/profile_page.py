from ui.pages.base_page import BasePage
from ui.locators.profile_locators import ProfileLocators


class ProfilePage(BasePage):

    locators = ProfileLocators()

    def change_profile_data(self, new_full_name, new_phone_number):
        self.find(self.locators.PROFILE_TITLE)
        full_name_input = self.find(self.locators.FULL_NAME_INPUT)
        phone_number_input = self.find(self.locators.PHONE_NUMBER_INPUT)
        full_name_input.clear()
        phone_number_input.clear()
        full_name_input.send_keys(new_full_name)
        phone_number_input.send_keys(new_phone_number)
        self.click(self.locators.SUBMIT_CHANGES_BUTTON)
