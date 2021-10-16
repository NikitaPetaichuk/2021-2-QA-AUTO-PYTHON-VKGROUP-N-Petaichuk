from selenium.webdriver.common.by import By


class CompaniesPageLocators:

    COMPANIES_PAGE_TITLE = (
        By.XPATH, '//div[contains(text(), "С чего начать?")]'
    )
