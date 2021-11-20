from ui.locators.skills_page_locators import SkillsPageLocators
from ui.pages.base_page import BasePage


class SkillsPage(BasePage):

    locators = SkillsPageLocators()

    def choose_skill(self, skill_text):
        skill_title_locator = self.locators.get_skill_title_locator(skill_text)
        self.swipe_to_element(skill_title_locator)
        self.click(skill_title_locator)
