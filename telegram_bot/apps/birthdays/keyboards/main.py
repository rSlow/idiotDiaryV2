from common.keyboards.base import BaseReplyKeyboardBuilder


class BirthdaysMainKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        check = "Проверить ДР 🎈"
        notifications = "Оповещения 🕓"
        clear_data = "Очистить данные 🗑"
        time_correction = "Установка часового пояса 🌏"

    buttons_list = [
        Buttons.check,
        Buttons.notifications,
        Buttons.clear_data,
        Buttons.time_correction,
    ]

    row_width = 2
