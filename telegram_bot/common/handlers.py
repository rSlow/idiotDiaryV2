from aiogram import types
from aiogram.fsm.context import FSMContext

from .FSM import CommonState
from .keyboards import StartKeyboard


async def start(message: types.Message, state: FSMContext):
    await state.set_state(CommonState.start)
    await message.answer(
        text="Куда надо?",
        reply_markup=StartKeyboard.build()
    )


async def delete(message: types.Message):
    await message.delete()
