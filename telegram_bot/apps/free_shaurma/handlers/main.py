from operator import itemgetter

from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import Context
from aiogram_dialog.widgets.kbd import Select, Button, Row
from aiogram_dialog.widgets.text import Const, Format

from common.buttons import CANCEL_BUTTON, BACK_BUTTON, MAIN_MENU_BUTTON
from ..FSM import FShStartFSM
from ..schemas.banks import ToBank
from ..settings import FSSettings


async def devices_getter(**__):
    devices = [
        (device.value.device_type.value, device.value.device_type.name)
        for device in FSSettings
    ]
    return {"devices": devices}


async def set_device(_: types.CallbackQuery,
                     __: Button,
                     manager: DialogManager,
                     device_id: str):
    manager.dialog_data.update({"device": device_id})
    await manager.next()


async def from_banks_getter(aiogd_context: Context, **__):
    device = aiogd_context.dialog_data.get("device")
    from_banks = [
        (bank.name_enum.value, bank.name_enum.name)
        for bank in
        FSSettings[device].value.from_banks
    ]
    return {"from_banks": from_banks}


async def set_from_bank(_: types.CallbackQuery,
                        __: Button,
                        manager: DialogManager,
                        from_bank_id: str):
    manager.dialog_data.update({"from_bank": from_bank_id})
    await manager.next()


async def to_banks_getter(aiogd_context: Context, **__):
    device = aiogd_context.dialog_data.get("device")
    from_bank = aiogd_context.dialog_data.get("from_bank")
    to_banks = [
        (bank.name_enum.value, bank.name_enum.name)
        for bank in
        FSSettings[device].value[from_bank].to_banks
    ]
    return {"to_banks": to_banks}


async def set_to_bank(_: types.CallbackQuery,
                      __: Button,
                      manager: DialogManager,
                      to_bank_id: str):
    data = manager.dialog_data
    data.update({"to_bank": to_bank_id})

    device = data["device"]
    from_bank = data["from_bank"]
    to_bank = data["to_bank"]

    bank_form: ToBank = FSSettings[device].value[from_bank][to_bank]
    form_states = bank_form.states_group
    await manager.start(form_states.first())


start_fsh_dialog = Dialog(
    Window(
        Const("(бес)платная шаурма. Выберите тип устройства:"),
        Select(
            Format("{item[0]}"),
            id="devices",
            item_id_getter=itemgetter(1),
            items="devices",
            on_click=set_device
        ),
        CANCEL_BUTTON,
        getter=devices_getter,
        state=FShStartFSM.device
    ),
    Window(
        Const("Выберите банк для перевода:"),
        Select(
            Format("{item[0]}"),
            id="from_banks",
            item_id_getter=itemgetter(1),
            items="from_banks",
            on_click=set_from_bank
        ),
        Row(BACK_BUTTON, MAIN_MENU_BUTTON),
        getter=from_banks_getter,
        state=FShStartFSM.from_bank
    ),
    Window(
        Const("Выберите банк для перевода:"),
        Select(
            Format("{item[0]}"),
            id="to_banks",
            item_id_getter=itemgetter(1),
            items="to_banks",
            on_click=set_to_bank
        ),
        Row(BACK_BUTTON, MAIN_MENU_BUTTON),
        getter=to_banks_getter,
        state=FShStartFSM.to_bank
    ),
)

# ---------- TEST ---------- #

