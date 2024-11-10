from abc import ABC
from dataclasses import dataclass

from idiotDiary.bot.utils.dialog_factory import InputForm
from .enums import BankName
from ..utils.types import RenderFunc


class FromBank(ABC):
    def __init__(self, *to_banks: "ToBank", name: BankName):
        self.to_banks = to_banks
        self.name = name

    def __getitem__(self, to_bank_enum_name: str) -> "ToBank":
        for to_bank in self.to_banks:
            if to_bank.name.name == to_bank_enum_name:
                return to_bank
        else:
            raise KeyError


class FromSberbank(FromBank):
    def __init__(self, *to_banks: "ToBank"):
        super().__init__(*to_banks, name=BankName.SBERBANK)


class FromTinkoff(FromBank):
    def __init__(self, *to_banks: "ToBank"):
        super().__init__(*to_banks, name=BankName.TINKOFF)


@dataclass
class ToBank(ABC):
    render_func: RenderFunc
    form: type[InputForm]
    name: BankName


@dataclass
class ToSberbank(ToBank):
    name: BankName = BankName.SBERBANK


@dataclass
class ToTinkoff(ToBank):
    name: BankName = BankName.TINKOFF
