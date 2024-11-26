from random import randint

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from idiotDiary.bot.utils.dialog_factory import InputForm, InputFormField
from .utils import type_factory as tf


async def get_random_amount_getter(dialog_manager: DialogManager, **__):
    random_amount = round(randint(1000000, 5000000) / 100, 2)
    data = {"random_amount": random_amount}
    dialog_manager.dialog_data.update(data)
    return data


async def random_amount_click(_, __, manager: DialogManager):
    random_amount = manager.dialog_data.get("random_amount")
    manager.dialog_data.update({"start_amount": random_amount})
    await manager.next()


class BaseTinkoffForm(InputForm):
    name = InputFormField(
        Const("Введите имя получателя:\n"),
        Const("Поддерживаемый формат:"),
        Const("Валерия Д."),
        Const("Валерия Демченко"),
        type_factory=tf.name_type_factory
    )
    phone_num = InputFormField(
        Const("Введите номер телефона:"),
        type_factory=tf.phone_type_factory
    )
    start_amount = InputFormField(
        Const("Введите начальную сумму (до перевода):"),
        Const("Либо нажми кнопку, чтобы подставить любое случайное значение от 10 до 50 тысяч:"),
        type_factory=tf.amount_type_factory,
        keyboard=Button(
            Format("{random_amount}"),
            id="random_amount",
            on_click=random_amount_click
        ),
        getter=get_random_amount_getter
    )
    transfer_amount = InputFormField(
        Const("Введите сумму перевода:"),
        type_factory=tf.amount_type_factory
    )


class AndroidTinkoffForm(BaseTinkoffForm):
    pass


class IPhoneTinkoffForm(BaseTinkoffForm):
    pass
