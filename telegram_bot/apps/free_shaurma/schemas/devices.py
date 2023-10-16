from abc import ABC
from dataclasses import dataclass, field
from typing import Iterable

from .banks import FromBank
from .enums import DeviceNames


@dataclass
class Device(ABC):
    from_banks: Iterable[FromBank]
    device_type: DeviceNames

    def find_bank(self, bank_name: str):
        for bank_obj in self.from_banks:
            if bank_obj.name_enum.name == bank_name:
                return bank_obj
        else:
            raise KeyError


@dataclass
class Android(Device):
    device_type: DeviceNames = field(default=DeviceNames.android)


@dataclass
class IPhone(Device):
    device_type: DeviceNames = field(default=DeviceNames.iphone)
