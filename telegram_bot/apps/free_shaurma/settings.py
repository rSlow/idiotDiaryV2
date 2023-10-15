from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Callable

from aiogram.fsm.state import StatesGroup

from .FSM import bank as FSMBank
from .utils import render


class ListEnum(Enum):
    @classmethod
    def as_name_list(cls):
        return [device.name for device in cls]

    @classmethod
    def as_value_list(cls):
        return [device.value for device in cls]

    @classmethod
    def find_from_value(cls, value: str):
        for attr in cls:
            if attr.value == value:
                return attr
        else:
            raise KeyError


class DeviceNames(ListEnum):
    android = "Android"
    iphone = "IPhone"


class BankNames(ListEnum):
    sberbank = "Сбербанк"
    tinkoff = "Тинькофф"


@dataclass
class ToBank:
    name_enum: BankNames
    render_func: Callable


@dataclass
class FromBank:
    state_group: type[StatesGroup]
    name_enum: BankNames
    to_banks: Iterable[ToBank]

    def find_bank(self, bank_name: str):
        for bank_obj in self.to_banks:
            if bank_obj.name_enum.value == bank_name:
                return bank_obj
        else:
            raise KeyError


@dataclass
class Device:
    device_type: DeviceNames
    from_banks: Iterable[FromBank]

    def find_bank(self, bank_name: str):
        for bank_obj in self.from_banks:
            if bank_obj.name_enum.name == bank_name:
                return bank_obj
        else:
            raise KeyError


class FSSettings(Enum):
    android = Device(
        device_type=DeviceNames.android,
        from_banks=[
            FromBank(
                name_enum=BankNames.sberbank,
                to_banks=[
                    ToBank(
                        name_enum=BankNames.sberbank,
                        render_func=render.android.sberbank.sberbank_sberbank_phone_android
                    )
                ],
                state_group=FSMBank.SberbankForm
            ),
            FromBank(
                name_enum=BankNames.tinkoff,
                to_banks=[
                    ToBank(
                        name_enum=BankNames.tinkoff,
                        render_func=render.android.tinkoff.tinkoff_tinkoff_phone_android
                    )
                ],
                state_group=FSMBank.TinkoffForm,
            ),
        ]
    )

    iphone = Device(
        device_type=DeviceNames.iphone,
        from_banks=[
            FromBank(
                name_enum=BankNames.sberbank,
                to_banks=[
                    ToBank(
                        name_enum=BankNames.sberbank,
                        render_func=render.iphone.sberbank.sberbank_sberbank_phone_iphone
                    )
                ],
                state_group=FSMBank.SberbankForm,
            ),
            FromBank(
                name_enum=BankNames.tinkoff,
                to_banks=[
                    ToBank(
                        name_enum=BankNames.tinkoff,
                        render_func=render.iphone.tinkoff.tinkoff_tinkoff_phone_iphone
                    )
                ],
                state_group=FSMBank.TinkoffForm
            ),
        ]
    )
