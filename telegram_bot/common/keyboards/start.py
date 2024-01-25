from .base import BaseReplyKeyboardBuilder
from .base_validators import ButtonWithValidator, IsOwnerValidator, BirthdaysAllowedValidator


class StartKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        not_working_place = "нерабочая площадка 😶‍🌫️"
        free_shaurma = "(бес)платная шаурма 🌯"
        birthdays = "напоминальщик ДР 🎂"
        music = "Музыка 🎧"
        admin = "Админка ⚙️"

    row_width = 1
    add_on_main_button = False
    buttons_list = [
        Buttons.not_working_place,
        Buttons.free_shaurma,
        ButtonWithValidator(
            text=Buttons.birthdays,
            validator=BirthdaysAllowedValidator()
        ),
        Buttons.music,
        ButtonWithValidator(
            text=Buttons.admin,
            validator=IsOwnerValidator()
        ),
    ]
