from common.base_keyboard import BaseKeyboardBuilder


class AdminKeyboard(BaseKeyboardBuilder):
    class Buttons:
        clear_birthdays = "Очистить дни рождения"

    row_width = 2
    buttons_list = [
        Buttons.clear_birthdays,
    ]
