from abc import ABC
from dataclasses import field, dataclass
from typing import Callable, Iterable

from common.dialogs import FormStatesGroup
from .enums import BankNames


@dataclass
class ToBank(ABC):
    render_func: Callable
    states_group: type[FormStatesGroup]
    name_enum: BankNames


@dataclass
class ToSberbank(ToBank):
    name_enum: BankNames = field(default=BankNames.sberbank)


@dataclass
class ToTinkoff(ToBank):
    name_enum: BankNames = field(default=BankNames.tinkoff)


@dataclass
class FromBank(ABC):
    to_banks: Iterable[ToBank]
    name_enum: BankNames

    def __getitem__(self, bank_name: str):
        for bank_obj in self.to_banks:
            if bank_obj.name_enum.name == bank_name:
                return bank_obj
        else:
            raise KeyError


@dataclass
class FromSberbank(FromBank):
    name_enum: BankNames = field(default=BankNames.sberbank)


@dataclass
class FromTinkoff(FromBank):
    name_enum: BankNames = field(default=BankNames.tinkoff)
