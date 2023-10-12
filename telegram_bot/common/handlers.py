from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from .FSM import CommonState
from .keyboards import StartKeyboard

router = Router()


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(CommonState.start)
    await message.answer(
        text="Куда надо?",
        reply_markup=StartKeyboard.build()
    )


@router.message(F.text)
async def delete(message: types.Message):
    await message.delete()
