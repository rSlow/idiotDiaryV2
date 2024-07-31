from enum import Enum


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
