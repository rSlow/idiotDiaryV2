from abc import ABC

from .banks import FromBank
from .enums import DeviceType


class Device(ABC):
    def __init__(self, *from_banks: FromBank, device_type: DeviceType) -> None:
        self.from_banks = from_banks
        self.type_ = device_type

    def __getitem__(self, from_bank_enum_name: str) -> FromBank:
        for bank_obj in self.from_banks:
            if bank_obj.name.name == from_bank_enum_name:
                return bank_obj
        else:
            raise KeyError


class Android(Device):
    def __init__(self, *from_banks: FromBank):
        super().__init__(*from_banks, device_type=DeviceType.ANDROID)


class IPhone(Device):
    def __init__(self, *from_banks: FromBank):
        super().__init__(*from_banks, device_type=DeviceType.IPHONE)
