from selenium.webdriver.common.by import By


class SegmentsLocators:

    SEGMENT_INSTRUCTION_TITLE = (By.XPATH, '//div[contains(@class, "instruction-module-title")]')
    SEGMENT_LIST_TITLE = (By.XPATH, '//div[contains(@class, "page_segments__title")]')

    CREATE_SEGMENT_LINK = (By.XPATH, '//a[@href = "/segments/segments_list/new/"]')
    CREATE_SEGMENT_BUTTON = (
        By.XPATH, '//div[contains(@class, "js-create-button-wrap")]/button[contains(@class, "button_submit")]'
    )

    ADDING_SEGMENT_CHECKBOX = (By.XPATH, '//input[contains(@class, "adding-segments-source__checkbox")]')
    ADDING_SEGMENT_SUBMIT = (By.XPATH, '//div[contains(@class, "adding-segments-modal__btn-wrap")]/button')
    SEGMENT_NAME_INPUT = (By.XPATH, '//div[contains(@class, "input_create-segment-form")]//input')
    SUBMIT_SEGMENT_BUTTON = (
        By.XPATH, '//div[contains(@class, "js-create-segment-button-wrap")]//button[@data-class-name = "Submit"]'
    )

    SEGMENTS_CHOOSE_ACTION_SELECT = (By.XPATH, '//div[contains(@class, "segmentsTable-module-massActionsSelect")]')
    DELETE_SEGMENTS_ACTION = (By.XPATH, '//li[contains(@class, "optionsList-module-option") and @data-test = "remove"]')

    @staticmethod
    def generate_segment_cell_locator(segment_name):
        return By.XPATH, f'//a[@title = "{segment_name}"]'

    @staticmethod
    def generate_segment_checkbox_locator(segment_id):
        return By.XPATH, f'//div[contains(@data-test, "row-{segment_id}")]//input[@type = "checkbox"]'
