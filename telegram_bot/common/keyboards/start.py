from .base import BaseKeyboardBuilder
from .base_validators import ButtonWithValidator, IsOwnerValidator


class StartKeyboard(BaseKeyboardBuilder):
    class Buttons:
        not_working_place = "нерабочая площадка 😶‍🌫️"
        free_shaurma = "(бес)платная шаурма 🌯"
        music = "Музыка 🎧"
        admin = "Админка ⚙️"

    row_width = 1
    add_on_main_button = False
    buttons_list = [
        Buttons.not_working_place,
        Buttons.free_shaurma,
        Buttons.music,
        ButtonWithValidator(
            text=Buttons.admin,
            validator=IsOwnerValidator()
        ),
    ]
