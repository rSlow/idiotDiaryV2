from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from common.filters import OwnerFilter
from ..FSM.admin import AdminStates
from ..keyboards.admin import AdminKeyboard
from common.keyboards.start import StartKeyboard
from common.FSM import CommonState
from ...not_working_place.ORM.birthdays import Birthday

admin_router = Router(name="admin")


@admin_router.message(
    F.text == StartKeyboard.Buttons.admin,
    OwnerFilter(),
    CommonState.start
)
async def start_admin(message: types.Message, state: FSMContext):
    await state.set_state(AdminStates.start)

    await message.answer(
        text="Выберите действие:",
        reply_markup=AdminKeyboard.build()
    )


@admin_router.message(
    F.text == AdminKeyboard.Buttons.clear_birthdays,
    AdminStates.start
)
async def clear_birthdays(message: types.Message):
    await Birthday.delete_data()

    await message.answer(
        text="Все дни рождения удалены.",
    )
