from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from ..FSM.bank_forms import TinkoffForm, SberbankForm, BankStatesGroup
from ..exceptions import ValidationError
from ..settings import FSSettings

bank_router = Router(name="bank_router")


@bank_router.message(
    F.text.as_("raw_value"),
    StateFilter(
        TinkoffForm,
        SberbankForm
    )
)
async def bank_cycle(message: types.Message, state: FSMContext, raw_state: str, raw_value: str):
    storage_data = await state.get_data()

    device_name: str = storage_data["device"]
    from_bank_name: str = storage_data["from_bank"]
    to_bank_name: str = storage_data["to_bank"]

    bank_state_group: BankStatesGroup = FSSettings[device_name].value.find_bank(from_bank_name).state_group
    current_bank_state = bank_state_group.get_by_raw(raw_state)
    state_name = raw_state.split(":")[1]
    try:
        validated_value = current_bank_state.validate(raw_value)

        data = await state.get_data()
        data["bank_values"][state_name] = validated_value
        await state.set_data(data)

        next_state = current_bank_state.next()
        if next_state is None:
            ...
        else:
            await state.set_state(next_state)
            await message.answer(
                text=next_state.start_text,
                reply_markup=next_state.keyboard.build()
            )
    except ValidationError as ex:
        await message.answer(
            text=current_bank_state.validator.error_text,
            reply_markup=current_bank_state.keyboard.build(),
        )
