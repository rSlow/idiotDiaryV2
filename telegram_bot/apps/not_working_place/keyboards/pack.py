from config.base_keyboard import BaseKeyboardBuilder


class PackKeyboard(BaseKeyboardBuilder):
    class Buttons:
        accept = "Запаковать!"

    buttons_list = [
        Buttons.accept
    ]


class PackAgainKeyboard(BaseKeyboardBuilder):
    class Buttons:
        again = "Еще один архив"

    buttons_list = [
        Buttons.again
    ]
