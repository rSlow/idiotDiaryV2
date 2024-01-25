import asyncio

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from ..utils import audio

from common.keyboards.base import CancelKeyboard
from common.utils.functions import get_now
from ..FSM.main import MusicState, YTDownloadState
from ..keyboards.main import MusicMainKeyboard
from common.FSM import CommonFSM
from common.keyboards.start import StartKeyboard

start_music_router = Router(name="start_music")


@start_music_router.message(
    CommonFSM.start,
    F.text == StartKeyboard.Buttons.music,
)
async def music_start(message: types.Message, state: FSMContext):
    await state.set_state(MusicState.start)
    await message.answer(
        text="Выберите действие:",
        reply_markup=MusicMainKeyboard.build()
    )
