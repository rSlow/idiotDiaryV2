from aiogram import types, F
from aiogram.fsm.context import FSMContext

from common.FSM import CommonState
from common.keyboards import StartKeyboard
from . import router
from ..FSM.start import Start
from ..keyboards.main import NotWorkingPlaceKeyboard


@router.message(
    F.text == StartKeyboard.Buttons.not_working_place,
    CommonState.start
)
async def start_main(message: types.Message, state: FSMContext):
    await main(
        message=message,
        state=state,
        text="(не)рабочая площадка. Выберите действие:"
    )


async def back_to_main(message: types.Message, state: FSMContext):
    await main(
        message=message,
        state=state,
        text="Возвращаю в главное меню площадки..."
    )


async def main(message: types.Message, text: str, state: FSMContext):
    await state.set_state(Start.main)

    await message.answer(
        text=text,
        reply_markup=NotWorkingPlaceKeyboard.build()
    )
