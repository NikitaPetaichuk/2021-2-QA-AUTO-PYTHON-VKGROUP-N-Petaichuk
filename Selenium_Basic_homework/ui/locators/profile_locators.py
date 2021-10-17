from selenium.webdriver.common.by import By


class ProfileLocators:

    PROFILE_TITLE = (
        By.XPATH, '//span[contains(text(), "Контактная информация")]'
    )
    FULL_NAME_INPUT = (
        By.XPATH, '//div[@data-name = "fio"]//input'
    )
    PHONE_NUMBER_INPUT = (
        By.XPATH, '//div[@data-name = "phone"]//input'
    )
    SUBMIT_CHANGES_BUTTON = (
        By.XPATH, '//button[contains(@class, "button_submit")]'
    )
    SUBMIT_MESSAGE = (
        By.XPATH, '//div[contains(text(), "Информация успешно сохранена")]'
    )
