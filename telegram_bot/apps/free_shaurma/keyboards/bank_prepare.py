from common.keyboards.base import BaseReplyKeyboardBuilder
from ..settings import FSSettings


class DeviceKeyboard(BaseReplyKeyboardBuilder):
    buttons_list = [device.value.device_type.value for device in FSSettings]


class FromBanksKeyboard(BaseReplyKeyboardBuilder):
    def __init__(self, device_name: str):
        super().__init__()
        self.buttons_list = [
            bank.name_enum.value
            for bank in
            FSSettings[device_name].value.from_banks
        ]


class ToBanksKeyboard(BaseReplyKeyboardBuilder):
    def __init__(self, device_name: str, bank_name: str):
        super().__init__()
        self.buttons_list = [
            bank.name_enum.value
            for bank in
            FSSettings[device_name].value.find_bank(bank_name).to_banks
        ]
