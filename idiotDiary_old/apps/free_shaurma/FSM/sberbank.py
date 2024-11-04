from aiogram_dialog.widgets.text import Const

from idiotDiary_old.common.dialogs.window_factory import FormState, \
    FormStatesGroup
from .. import validators


class BaseSberbankForm(FormStatesGroup, abstract=True):
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


class AndroidSberbankForm(BaseSberbankForm):
    pass


class IPhoneSberbankForm(BaseSberbankForm):
    pass
