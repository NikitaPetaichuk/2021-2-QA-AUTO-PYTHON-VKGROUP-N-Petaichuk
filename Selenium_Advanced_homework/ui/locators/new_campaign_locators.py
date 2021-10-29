from selenium.webdriver.common.by import By


class NewCampaignLocators:

    TRAFFIC_CONVERSION = (By.XPATH, '//div[contains(@class, "_traffic")]')
    TARGETING_URL = (By.XPATH, '//input[contains(@class, "mainUrl-module-searchInput")]')
    CAMPAIGN_NAME_INPUT = (By.XPATH, '//div[contains(@class, "input_campaign-name")]//input')
    BANNER_PATTERN_CHOOSE = (By.XPATH, '//div[contains(@id, "patterns_banner")]')
    PICTURE_INPUT = (By.XPATH, '//div[contains(@class, "roles-module-currentPatternButton")]//input[@type = "file"]')
    SUBMIT_CAMPAIGN_BUTTON = (
        By.XPATH, '//div[contains(@class, "js-save-button-wrap")]//button[@data-class-name = "Submit"]'
    )
