from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from common.FSM import CommonFSM
from common.filters import OwnerFilter
from common.keyboards.start import StartKeyboard
from .. import settings
from ..FSM.bank_forms import ChooseBankParams
from ..FSM.modified_state import BankStatesGroup
from ..keyboards.bank_prepare import FromBanksKeyboard, ToBanksKeyboard, DeviceKeyboard
from ..schemas import enums
from ..settings import FSSettings
from ..utils import send_files

start_fsh_router = Router(name="start_fsh")


@start_fsh_router.message(
    CommonFSM.start,
    F.text == StartKeyboard.Buttons.free_shaurma,
)
async def choose_device(message: types.Message, state: FSMContext):
    await state.set_state(ChooseBankParams.device)

    await message.answer(
        text="(бес)платная шаурма. Выберите тип устройства:",
        reply_markup=DeviceKeyboard.build()
    )


@start_fsh_router.message(
    ChooseBankParams.device,
    F.text[F.in_(enums.DeviceNames.as_value_list())].as_("device_value"),
)
async def choose_from_bank(message: types.Message, state: FSMContext, device_value: str):
    device_enum = enums.DeviceNames.find_from_value(device_value)
    await state.update_data(device=device_enum.name)

    await state.set_state(ChooseBankParams.from_bank)

    await message.answer(
        text="Выберите банк для перевода:",
        reply_markup=FromBanksKeyboard.build(
            device_name=device_enum.name
        )
    )


@start_fsh_router.message(
    ChooseBankParams.from_bank,
    F.text[F.in_(enums.BankNames.as_value_list())].as_("from_bank_value"),
)
async def choose_to_bank(message: types.Message, state: FSMContext, from_bank_value: str):
    storage_data = await state.get_data()
    device = storage_data["device"]

    from_bank_name = enums.BankNames.find_from_value(from_bank_value).name

    await state.update_data(from_bank=from_bank_name)

    await state.set_state(ChooseBankParams.to_bank)

    await message.answer(
        text="Куда переводим?",
        reply_markup=ToBanksKeyboard.build(
            device_name=device,
            bank_name=from_bank_name,
        )
    )


@start_fsh_router.message(
    ChooseBankParams.to_bank,
    F.text[F.in_(enums.BankNames.as_value_list())].as_("to_bank_value"),
)
async def start_bank_cycle(message: types.Message, state: FSMContext, to_bank_value: str):
    storage_data = await state.get_data()

    device_name: str = storage_data["device"]
    from_bank_name: str = storage_data["from_bank"]
    to_bank_name: str = enums.BankNames.find_from_value(to_bank_value).name
    await state.update_data(to_bank=to_bank_name)

    bank_state_group: BankStatesGroup = settings.FSSettings[device_name].value.find_bank(from_bank_name).state_group

    await state.update_data({"bank_values": {}})

    start_bank_state = bank_state_group.first()
    await state.set_state(start_bank_state)
    await message.answer(
        text=start_bank_state.start_text,
        reply_markup=start_bank_state.keyboard.build()
    )


# ---------- TEST ---------- #

@start_fsh_router.message(
    ChooseBankParams.device,
    OwnerFilter(),
    Command("test"),
)
async def test(message: types.Message):
    from_bank_name = "tinkoff"
    to_bank_name = "tinkoff"
    device_name = "iphone"

    render_func = FSSettings[device_name].value.find_bank(from_bank_name).find_bank(to_bank_name).render_func

    image_io = render_func(
        name="Евгений П.",
        phone_num="+7 (914) 665-64-93",
        start_sum=25434.56,
        transfer_sum=250
    )

    await send_files.send_file(
        image_io=image_io,
        message=message,
        from_bank=from_bank_name,
        to_bank=to_bank_name,
        device=device_name
    )
