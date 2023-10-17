from config import settings
from .base_keyboard import BaseKeyboardBuilder


class StartKeyboard(BaseKeyboardBuilder):
    class Buttons:
        not_working_place = "нерабочая площадка 😶‍🌫️"
        free_shaurma = "(бес)платная шаурма 🌯"
        admin = "Админка"

    row_width = 1
    add_on_main_button = False
    buttons_list = [
        Buttons.not_working_place,
        Buttons.free_shaurma,
    ]

    def __init__(self, user_id: int | str):
        super().__init__()
        if str(user_id) == settings.OWNER_ID:
            self.buttons_list = self.buttons_list.copy()
            self.buttons_list.append(self.Buttons.admin)
