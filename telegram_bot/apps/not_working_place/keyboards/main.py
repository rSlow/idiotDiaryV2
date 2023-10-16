from common.base_keyboard import BaseKeyboardBuilder


class NotWorkingPlaceKeyboard(BaseKeyboardBuilder):
    class Buttons:
        pack = "Запаковать 💼"
        morph = "Склонения 💬"
        download_video_note = "Скачать кружочек 📹"
        convert_voice = "Конвертировать голосовое 🎤"
        check_birthdays = "Проверить ДР 🎈"

    buttons_list = [
        Buttons.pack,
        Buttons.morph,
        Buttons.download_video_note,
        Buttons.convert_voice,
        Buttons.check_birthdays,
    ]
