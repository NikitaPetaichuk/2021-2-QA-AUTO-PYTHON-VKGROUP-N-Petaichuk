from selenium.webdriver.common.by import By


class CampaignsLocators:
    CREATE_CAMPAIGN_LINK = (By.XPATH, '//a[@href = "/campaign/new"]')
    CREATE_CAMPAIGN_BUTTON = (
        By.XPATH,
        '//div[contains(@class, "dashboard-module-createButtonWrap")]/div[contains(@class, "button-module-button")]'
    )

    GO_TO_SEGMENTS_BUTTON = (By.XPATH, '//a[@href = "/segments"]')

    CAMPAIGN_CHOOSE_ACTION_SELECT = (By.XPATH, '//div[contains(@class, "tableControls-module-massActionsSelect")]')
    DELETE_CAMPAIGNS_ACTION = (By.XPATH, '//li[contains(@class, "optionsList-module-option") and @data-test = "8"]')
    NOTIFY_SUCCESS_MESSAGE = (By.XPATH, '//div[contains(@class, "notify-module-success")]')

    @staticmethod
    def generate_campaign_cell_locator(campaign_name):
        return By.XPATH, f'//a[contains(@class, "nameCell-module-campaignNameLink") and @title = "{campaign_name}"]'

    @staticmethod
    def generate_campaign_checkbox_locator(campaign_id):
        return By.XPATH, f'//div[contains(@data-test, "row-{campaign_id}")]//input[@type = "checkbox"]'
