from random import randint

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from common.dialogs import FormStatesGroup, FormState
from .. import validators


async def get_random_sum(dialog_manager: DialogManager, **__):
    random_sum = round(randint(1000000, 5000000) / 100, 2)
    data = {"random_sum": random_sum}
    dialog_manager.dialog_data.update(data)
    return data


async def random_sum_click(_: CallbackQuery,
                           __: Button,
                           manager: DialogManager):
    random_sum = manager.dialog_data.get("random_sum")
    manager.dialog_data.update({"start_sum": random_sum})
    await manager.next()


class TinkoffForm(FormStatesGroup):
    name = FormState(
        Const("Введите имя получателя:\n\n"
              "Поддерживаемый формат:\n"
              "Валерия Д.\n"
              "Валерия Демченко"),
        type_factory=validators.NameTypeFactory
    )
    phone_num = FormState(
        Const("Введите номер телефона:"),
        type_factory=validators.PhoneTypeFactory
    )
    start_sum = FormState(
        Const("Введите начальную сумму (до перевода):"),
        Const("Либо нажми кнопку, чтобы подставить любое случайное значение от 10 до 50 тысяч:"),
        type_factory=validators.SumTypeFactory,
        keyboard=Button(
            Format("{random_sum}"),
            id="random_sum",
            on_click=random_sum_click
        ),
        getter=get_random_sum
    )
    transfer_sum = FormState(
        Const("Введите сумму перевода:"),
        type_factory=validators.SumTypeFactory
    )
