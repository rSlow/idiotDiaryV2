from common.keyboards.base import BaseReplyKeyboardBuilder


class AdminKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        clear_birthdays = "Очистить дни рождения"

    row_width = 2
    buttons_list = [
        Buttons.clear_birthdays,
    ]
