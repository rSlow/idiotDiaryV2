from .base_keyboard import BaseKeyboardBuilder


class StartKeyboard(BaseKeyboardBuilder):
    class Buttons:
        not_working_place = "нерабочая площадка 😶‍🌫️"
        free_shaurma = "(бес)платная шаурма 🌯"

    row_width = 1
    add_on_main_button = False
    buttons_list = [
        Buttons.not_working_place,
        Buttons.free_shaurma,
    ]
