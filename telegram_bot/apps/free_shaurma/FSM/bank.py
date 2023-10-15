from aiogram.fsm.state import StatesGroup, State

from .modified_state import BankStatesGroup, BankState
from ..keyboards.bank_cycle import RandomSumKeyboard
from .. import validators


class ChooseBankParams(StatesGroup):
    device = State()
    from_bank = State()
    to_bank = State()


class TinkoffForm(BankStatesGroup):
    name = BankState(
        start_text="Введите имя получателя:\n\n"
                   "Поддерживаемый формат:\n"
                   "Валерия Д.\n"
                   "Валерия Демченко",
        validator=validators.NameValidator()
    )
    phone_num = BankState(
        start_text="Введите номер телефона:",
        validator=validators.PhoneValidator()
    )
    start_sum = BankState(
        start_text="Введите начальную сумму (до перевода):\n"
                   "Либо нажми кнопку, чтобы подставить любое случайное значение от 10 до 50 тысяч",
        keyboard=RandomSumKeyboard,
        validator=validators.SumValidator()
    )
    transfer_sum = BankState(
        start_text="Введите сумму перевода:",
        validator=validators.SumValidator()
    )


class SberbankForm(BankStatesGroup):
    name = BankState(
        start_text="Введите имя:\n\n"
                   "Поддерживаемый формат:\n"
                   "Валерия Владимировна Д.\n"
                   "Валерия Владимировна Демченко",
        validator=validators.NameValidator()
    )
    transfer_sum = BankState(
        start_text="Введите сумму перевода:",
        validator=validators.SumValidator()
    )
