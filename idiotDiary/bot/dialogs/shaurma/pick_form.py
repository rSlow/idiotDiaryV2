from operator import attrgetter

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Row
from aiogram_dialog.widgets.text import Const, Format

from idiotDiary.bot.forms.shaurma import FshBankForms
from idiotDiary.bot.states.shaurma import FshPickFormSG
from idiotDiary.bot.views import buttons as b


async def devices_getter(**__):
    devices = [device.type_ for device in FshBankForms]
    return {"devices": devices}


async def set_device(_, __, manager: DialogManager, device_id: str):
    manager.dialog_data.update({"device": device_id})
    await manager.next()


set_device_window = Window(
    Const("(бес)платная шаурма. Выберите тип устройства:"),
    Select(
        Format("{item.value}"),
        id="devices",
        item_id_getter=attrgetter("name"),
        items="devices",
        on_click=set_device
    ),
    b.CANCEL,
    getter=devices_getter,
    state=FshPickFormSG.device
)


async def from_banks_getter(dialog_manager: DialogManager, **__):
    device_name = dialog_manager.dialog_data.get("device")
    from_banks = [bank.name for bank in FshBankForms[device_name].from_banks]
    return {"from_banks": from_banks}


async def set_from_bank(_, __, manager: DialogManager, from_bank_id: str):
    manager.dialog_data.update({"from_bank": from_bank_id})
    await manager.next()


from_bank_window = Window(
    Const("Выберите банк для перевода:"),
    Select(
        Format("{item.value}"),
        id="from_banks",
        item_id_getter=attrgetter("name"),
        items="from_banks",
        on_click=set_from_bank
    ),
    Row(b.BACK, b.MAIN_MENU),
    getter=from_banks_getter,
    state=FshPickFormSG.from_bank
)


async def to_banks_getter(dialog_manager: DialogManager, **__):
    device = dialog_manager.dialog_data.get("device")
    from_bank = dialog_manager.dialog_data.get("from_bank")
    to_banks = [
        to_bank.name
        for to_bank in FshBankForms[device][from_bank].to_banks
    ]
    return {"to_banks": to_banks}


async def set_to_bank(_, __, manager: DialogManager, to_bank_id: str):
    data = manager.dialog_data
    data.update({"to_bank": to_bank_id})

    device = data["device"]
    from_bank = data["from_bank"]
    to_bank = data["to_bank"]

    bank_dialog = FshBankForms[device][from_bank][to_bank]
    await manager.start(bank_dialog.form.first())


to_bank_window = Window(
    Const("Выберите банк для перевода:"),
    Select(
        Format("{item.value}"),
        id="to_banks",
        item_id_getter=attrgetter("name"),
        items="to_banks",
        on_click=set_to_bank
    ),
    Row(b.BACK, b.MAIN_MENU),
    getter=to_banks_getter,
    state=FshPickFormSG.to_bank
)

pick_fsh_form_dialog = Dialog(
    set_device_window,
    from_bank_window,
    to_bank_window
)
