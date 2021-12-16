from ui.locators.main_page_locators import MainPageLocators
from ui.pages.base_page import BasePage


class MainPage(BasePage):

    locators = MainPageLocators()

    def logout(self):
        self.click(self.locators.LOGOUT_BUTTON)

    def get_user_name(self):
        user_name_label = self.find(self.locators.USERNAME_LABEL)
        return user_name_label.text.split()[-1]

    def get_vk_id_value(self):
        vk_id_label = self.find(self.locators.VK_ID_LABEL)
        if vk_id_label.text:
            vk_id = vk_id_label.text.split()[-1]
        else:
            vk_id = None
        return vk_id

    def go_home(self, click_on_logo=True):
        if click_on_logo:
            self.click(self.locators.BRAND_LOGO)
        else:
            self.click(self.locators.HOME_BUTTON)

    def go_from_section(self, section_button_locator, link_for_locator=None):
        if link_for_locator is None:
            self.click(section_button_locator)
        else:
            action_chain = self.action_chains
            section_button = self.find(section_button_locator)
            action_chain.move_to_element(section_button).perform()

            link_locator = self.locators.get_link_locator(link_for_locator)
            link_to_go = self.find(link_locator)
            action_chain.click(link_to_go).perform()

    def go_by_main_button(self, link_for_button):
        link_locator = self.locators.get_link_locator(link_for_button)
        self.click(link_locator)
