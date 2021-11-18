from appium.webdriver.common.mobileby import MobileBy


class MainPageLocators:

    GO_TO_MENU_BUTTON = (MobileBy.ID, "ru.mail.search.electroscope:id/assistant_menu_bottom")

    KEYBOARD_BUTTON = (MobileBy.ID, "ru.mail.search.electroscope:id/keyboard")
    COMMAND_INPUT = (MobileBy.ID, "ru.mail.search.electroscope:id/input_text")
    SEND_COMMAND = (MobileBy.ID, "ru.mail.search.electroscope:id/text_input_action")

    SHOW_ALL_SKILLS = (MobileBy.ID, "ru.mail.search.electroscope:id/item_skill_card_action_show_all")

    SUGGESTIONS_LIST = (
        MobileBy.XPATH,
        '//androidx.recyclerview.widget.RecyclerView[@resource-id = "ru.mail.search.electroscope:id/suggests_list"]'
    )

    @staticmethod
    def get_fact_card_title_locator(fact_card_title_text):
        return (
            MobileBy.XPATH,
            '//android.widget.TextView[@resource-id = "ru.mail.search.electroscope:id/item_dialog_fact_card_title" and '
            f'contains(@text, "{fact_card_title_text}")]'
        )

    @staticmethod
    def get_suggestion_locator(suggestion_text):
        return (
            MobileBy.XPATH,
            '//android.widget.TextView[@resource-id = "ru.mail.search.electroscope:id/item_suggest_text" and '
            f'contains(@text, "{suggestion_text}")]'
        )

    @staticmethod
    def get_message_locator(message_text):
        return (
            MobileBy.XPATH,
            '//android.widget.TextView[@resource-id = "ru.mail.search.electroscope:id/dialog_item" and '
            f'contains(@text, "{message_text}")]'
        )

    @staticmethod
    def get_player_track_title_locator(player_track_title_text):
        return (
            MobileBy.XPATH,
            '//android.widget.TextView[@resource-id = "ru.mail.search.electroscope:id/player_track_name" and '
            f'contains(@text, "{player_track_title_text}")] '
        )
