from common.keyboards.base import BaseReplyKeyboardBuilder


class AdminKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        clear_birthdays = "Очистить дни рождения"
        get_logs = "Файлы логов"

    row_width = 2
    buttons_list = [
        Buttons.clear_birthdays,
        Buttons.get_logs,
    ]
