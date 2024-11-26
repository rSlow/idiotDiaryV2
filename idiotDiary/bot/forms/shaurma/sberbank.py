from aiogram_dialog.widgets.text import Const

from idiotDiary.bot.utils.dialog_factory import InputForm, InputFormField
from .utils import type_factory as tf


class BaseSberbankForm(InputForm):
    name = InputFormField(
        Const("Введите имя:\n"),
        Const("Поддерживаемый формат:"),
        Const("Валерия Владимировна Д."),
        Const("Валерия Владимировна Демченко"),
        type_factory=tf.name_type_factory,
        # error_message=... # TODO
    )
    transfer_amount = InputFormField(
        Const("Введите сумму перевода:"),
        type_factory=tf.amount_type_factory
    )


class AndroidSberbankForm(BaseSberbankForm):
    pass


class IPhoneSberbankForm(BaseSberbankForm):
    pass
