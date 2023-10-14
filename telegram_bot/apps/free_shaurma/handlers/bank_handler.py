from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from .. import settings
from ..FSM.bank import ChooseBankParams, BankStatesGroup

bank_router = Router(name="bank_router")


@bank_router.message(
    F.text[F.in_(settings.BankNames.as_value_list())].as_("to_bank"),
    StateFilter(ChooseBankParams.to_bank, BankStatesGroup)
)
async def bank_cycle(message: types.Message, state: FSMContext, to_bank: str):
    storage_data = await state.get_data()

    device_name: str = storage_data["device"]
    from_bank_name: str = storage_data["bank"]
    to_bank_name: str = settings.BankNames.find_from_value(to_bank).name
    bank_state_group: BankStatesGroup = storage_data["bank_state_group"]

    await state.update_data({"state_attrs": {}})

    next_state = BankStatesGroup.next()
    if next_state is False:
        ...
    else:
        await state.set_state(next_state)
