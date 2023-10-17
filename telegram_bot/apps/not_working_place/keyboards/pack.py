from common.keyboards.base import BaseKeyboardBuilder


class PackKeyboard(BaseKeyboardBuilder):
    class Buttons:
        accept = "Запаковать!"

    buttons_list = [
        Buttons.accept
    ]


class PackFinishKeyboard(BaseKeyboardBuilder):
    class Buttons:
        again = "Еще один архив"

    buttons_list = [
        Buttons.again
    ]
