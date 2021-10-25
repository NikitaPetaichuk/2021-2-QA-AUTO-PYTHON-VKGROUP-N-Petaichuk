from selenium.webdriver.common.by import By


class SegmentsLocators:

    SEGMENT_INSTRUCTION_TITLE = (
        By.XPATH, '//div[contains(@class, "instruction-module-title")]'
    )
    SEGMENT_LIST_TITLE = (
        By.XPATH, '//div[contains(@class, "page_segments__title")]'
    )

    CREATE_SEGMENT_LINK = (
        By.XPATH, '//a[@href = "/segments/segments_list/new/"]'
    )
    CREATE_SEGMENT_BUTTON = (
        By.XPATH, '//div[contains(@class, "js-create-button-wrap")]/button[contains(@class, "button_submit")]'
    )

    ADDING_SEGMENT_CHECKBOX = (
        By.XPATH, '//input[contains(@class, "adding-segments-source__checkbox")]'
    )
    ADDING_SEGMENT_SUBMIT = (
        By.XPATH, '//div[contains(@class, "adding-segments-modal__btn-wrap")]/button'
    )
    SEGMENT_NAME_INPUT = (
        By.XPATH, '//div[contains(@class, "input_create-segment-form")]//input'
    )
    SUBMIT_SEGMENT_BUTTON = (
        By.XPATH,
        '//div[contains(@class, "js-create-segment-button-wrap")]//button[@data-class-name = "Submit"]'
    )

    SEGMENT_CELL_TEMPLATE = '//a[@title = "{}"]'
    SEGMENTS_TABLE_SCROLL = (
        By.XPATH, '//div[@class = "custom-scroll__handler"]'
    )
    SEGMENT_DELETE_BUTTON_TEMPLATE =\
        '//div[contains(@data-test, "remove-{}")]//span[contains(@class, "cells-module-removeCell")]'
    REMOVE_SUBMIT_BUTTON = (
        By.XPATH, '//button[contains(@class, "button_confirm-remove")]'
    )
