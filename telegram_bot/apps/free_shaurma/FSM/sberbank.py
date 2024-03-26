from aiogram_dialog.widgets.text import Const

from common.dialogs import FormStatesGroup, FormState
from .. import validators


class SberbankForm(FormStatesGroup):
    name = FormState(
        Const("Введите имя:\n\n"
              "Поддерживаемый формат:\n"
              "Валерия Владимировна Д.\n"
              "Валерия Владимировна Демченко"),
        type_factory=validators.NameTypeFactory
    )
    transfer_sum = FormState(
        Const("Введите сумму перевода:"),
        type_factory=validators.SumTypeFactory
    )
