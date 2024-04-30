from aiogram import Router, types
from aiogram.filters import Command
from common.filters import OwnerFilter
from ..schemas.enums import DeviceNames, BankNames
from ..settings import FSSettings
from ..utils import send_files

test_fsh_router = Router(name="test_fsh")


@test_fsh_router.message(
    OwnerFilter(),
    Command("test_fsh"),
)
async def test(message: types.Message):
    from_bank_name = BankNames.tinkoff.name
    to_bank_name = BankNames.tinkoff.name
    device_name = DeviceNames.iphone.name

    render_func = FSSettings[device_name].value[from_bank_name][to_bank_name].render_func

    data = {
        "name": "Максим М.",
        "phone_num": "+7 (914) 665-64-93",
        "start_sum": 25434.56,
        "transfer_sum": 250
    }

    await send_files.send_file(
        message=message,
        render_func=render_func,
        data=data
    )
