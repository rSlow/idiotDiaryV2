from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from ..FSM.admin import AdminStates
from ..filters import UserIDFilter
from ..keyboards.admin import AdminKeyboard
from common.keyboards import StartKeyboard
from common.FSM import CommonState
from config import settings
from ...not_working_place.ORM.birthdays import Birthday

admin_router = Router(name="admin")


@admin_router.message(
    F.text == StartKeyboard.Buttons.admin,
    UserIDFilter(users_id=settings.OWNER_ID),
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
