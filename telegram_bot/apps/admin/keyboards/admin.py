from common.keyboards.base import BaseReplyKeyboardBuilder


class AdminKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        get_logs = "Файлы логов"

    row_width = 2
    buttons_list = [
        Buttons.get_logs,
    ]
