from common.keyboards.base import BaseReplyKeyboardBuilder


class PackKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        accept = "Запаковать!"

    buttons_list = [
        Buttons.accept
    ]


class PackFinishKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        again = "Еще один архив"

    buttons_list = [
        Buttons.again
    ]
