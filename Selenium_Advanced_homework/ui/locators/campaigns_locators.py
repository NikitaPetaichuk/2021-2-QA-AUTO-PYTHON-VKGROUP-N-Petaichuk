from selenium.webdriver.common.by import By


class CampaignsLocators:

    CREATE_CAMPAIGN_LINK = (
        By.XPATH, '//a[@href = "/campaign/new"]'
    )
    CREATE_CAMPAIGN_BUTTON = (
        By.XPATH,
        '//div[contains(@class, "dashboard-module-createButtonWrap")]/div[contains(@class, "button-module-button")]'
    )
    CAMPAIGN_TABLE_CELL_TEMPLATE = '//a[contains(@class, "nameCell-module-campaignNameLink") and @title = "{}"]'
    GO_TO_SEGMENTS_BUTTON = (
        By.XPATH, '//a[@href = "/segments"]'
    )