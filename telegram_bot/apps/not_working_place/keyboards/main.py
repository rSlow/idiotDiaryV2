from common.keyboards.base import BaseReplyKeyboardBuilder
from common.keyboards.base_validators import ButtonWithValidator, IsOwnerValidator


class NotWorkingPlaceKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        pack = "Запаковать 💼"
        morph = "Склонения 💬"
        download_video_note = "Скачать кружочек 📹"
        convert_voice = "Конвертировать голосовое 🎤"
        check_birthdays = "Проверить ДР 🎈"
        inn_parse = "Узнать ИНН 📇"

    buttons_list = [
        Buttons.pack,
        Buttons.morph,
        Buttons.download_video_note,
        Buttons.convert_voice,
        ButtonWithValidator(
            text=Buttons.check_birthdays,
            validator=IsOwnerValidator()
        ),
        Buttons.inn_parse,
    ]
