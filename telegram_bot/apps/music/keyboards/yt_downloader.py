from common.keyboards.base import BaseReplyKeyboardBuilder


class TimecodeKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        full = "Полностью"

    buttons_list = [
        Buttons.full
    ]
    one_time_keyboard = True
