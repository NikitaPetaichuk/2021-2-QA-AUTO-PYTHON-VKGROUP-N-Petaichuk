from selenium.webdriver.common.by import By


def create_xpath_one_value_locator(template, value):
    locator_xpath = template.format(value)
    return By.XPATH, locator_xpath
