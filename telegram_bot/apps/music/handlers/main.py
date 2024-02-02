from typing import Optional

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from common.FSM import CommonFSM
from common.keyboards.start import StartKeyboard
from ..FSM.main import MusicState
from ..keyboards.main import MusicMainKeyboard

start_music_router = Router(name="start_music")


@start_music_router.message(
    CommonFSM.start,
    F.text == StartKeyboard.Buttons.music,
)
async def music_start(message: types.Message,
                      state: FSMContext,
                      text: Optional[str]):
    await state.set_state(MusicState.start)
    await message.answer(
        text=text or "Выберите действие:",
        reply_markup=MusicMainKeyboard.build()
    )
