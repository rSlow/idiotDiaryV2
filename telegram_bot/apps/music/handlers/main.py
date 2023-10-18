import asyncio

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

from common.keyboards.base import CancelKeyboard
from common.utils.functions import get_now
from ..FSM.main import MusicState, MusicDownloadState
from ..keyboards.main import MusicMainKeyboard
from common.FSM import CommonState
from common.keyboards.start import StartKeyboard
from ..utils.download_audio import download_audio

start_music_router = Router(name="start_music")


@start_music_router.message(
    F.text == StartKeyboard.Buttons.music,
    CommonState.start
)
async def music_start(message: types.Message, state: FSMContext):
    await state.set_state(MusicState.start)
    await message.answer(
        text="Выберите действие",
        reply_markup=MusicMainKeyboard.build()
    )


@start_music_router.message(
    F.text == MusicMainKeyboard.Buttons.download_from_yt,
    MusicState.start
)
async def start_download_audio(message: types.Message, state: FSMContext):
    await state.set_state(MusicDownloadState.wait_url)
    await message.answer(
        text="Ожидаю ссылку на YouTube видео...",
        reply_markup=CancelKeyboard.build()
    )


@start_music_router.message(
    F.text.as_("url"),
    MusicDownloadState.wait_url
)
async def download(message: types.Message, state: FSMContext, url: str):
    await state.set_state(MusicDownloadState.download)
    audio_io = await asyncio.to_thread(download_audio, url)
    audio = BufferedInputFile(
        file=audio_io.read(),
        filename=f"{get_now():%d_%m_%y__%H_%M_%S}.mp3"
    )

    await message.answer_document(document=audio)
    await music_start(
        message=message,
        state=state
    )
