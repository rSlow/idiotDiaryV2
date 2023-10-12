from common.base_keyboard import BaseKeyboardBuilder


class ConvertVideoKeyboard(BaseKeyboardBuilder):
    pass


class ConvertAgainVideoKeyboard(BaseKeyboardBuilder):
    class Buttons:
        again = "Еще одно 🔄"

    buttons_list = [
        Buttons.again
    ]
