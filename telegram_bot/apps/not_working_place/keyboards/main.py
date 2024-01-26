from common.keyboards.base import BaseReplyKeyboardBuilder


class NotWorkingPlaceKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        pack = "Запаковать 💼"
        morph = "Склонения 💬"
        download_video_note = "Скачать кружочек 📹"
        convert_voice = "Конвертировать голосовое 🎤"
        inn_parse = "Узнать ИНН 📇"

    buttons_list = [
        Buttons.pack,
        Buttons.morph,
        Buttons.download_video_note,
        Buttons.convert_voice,
        Buttons.inn_parse,
    ]
