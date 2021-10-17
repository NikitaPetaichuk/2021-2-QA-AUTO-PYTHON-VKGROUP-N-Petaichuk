from selenium.webdriver.common.by import By


class CampaignsPageLocators:

    CAMPAIGNS_PAGE_TITLE = (
        By.XPATH, '//div[contains(text(), "С чего начать?")]'
    )
