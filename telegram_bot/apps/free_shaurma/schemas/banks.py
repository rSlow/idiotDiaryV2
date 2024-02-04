from abc import ABC
from dataclasses import field, dataclass
from typing import Callable, Iterable

from .enums import BankNames
from ..FSM import bank_forms
from ..FSM.modified_state import BankStatesGroup


@dataclass
class ToBank(ABC):
    render_func: Callable
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
    state_group: type[BankStatesGroup]
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
    state_group: type[BankStatesGroup] = field(default=bank_forms.SberbankForm)


@dataclass
class FromTinkoff(FromBank):
    name_enum: BankNames = field(default=BankNames.tinkoff)
    state_group: type[BankStatesGroup] = field(default=bank_forms.TinkoffForm)
