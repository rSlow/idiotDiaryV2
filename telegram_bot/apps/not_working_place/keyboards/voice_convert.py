from common.keyboards.base import BaseReplyKeyboardBuilder


class ConvertVideoKeyboard(BaseReplyKeyboardBuilder):
    pass


class ConvertAgainVideoKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        again = "Еще одно 🔄"

    buttons_list = [
        Buttons.again
    ]
