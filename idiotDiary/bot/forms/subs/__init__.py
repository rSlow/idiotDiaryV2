from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from idiotDiary.bot.services.subs.check_url import on_url_success
from idiotDiary.bot.utils.dialog_factory import InputForm, InputFormField
from . import type_factory as tf


async def on_default_frequency(_, __, manager: DialogManager):
    manager.dialog_data["frequency"] = 60
    await manager.next()


class SubCreateForm(InputForm):
    url = InputFormField(
        Const("Ожидаю ссылку подписки в формате:"),
        Const("https://www.farpost.ru/..."),
        Const("Введенный запрос будет проверен на правильность автоматически."),
        type_factory=tf.url_validator,
        on_success=on_url_success,
        error_message="Неверная ссылка: {message.text}"
    )
    frequency = InputFormField(
        Const("Ссылка прошла проверку!"),
        Const("Укажите периодичность проверки в секундах (цифрой), не менее 30 секунд:"),
        type_factory=tf.frequency_validator,
        keyboard=Button(
            text=Const("Значение по умолчанию (60 секунд)"),
            id="default_frequency",
            on_click=on_default_frequency
        )
    )
    name = InputFormField(
        Const("Введите название подписки:")
    )
