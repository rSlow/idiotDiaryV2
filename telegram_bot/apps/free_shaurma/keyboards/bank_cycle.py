from random import randint

from common.keyboards.base import BaseKeyboardBuilder


class RandomSumKeyboard(BaseKeyboardBuilder):
    buttons_list = [
        f"{randint(1000000, 5000000) / 100:.2f}"
    ]
