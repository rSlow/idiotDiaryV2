import asyncio

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

from common.utils.sync_to_async import set_async
from .main import music_start
from .. import settings
from ..keyboards.main import MusicMainKeyboard
from ..utils import audio

from common.keyboards.base import CancelKeyboard
from ..FSM.main import MusicState, YTDownloadState

music_yt_router = Router(name="music_yt")


@music_yt_router.message(
    F.text == MusicMainKeyboard.Buttons.download_from_yt,
    MusicState.start
)
async def start_download_audio(message: types.Message, state: FSMContext):
    await state.set_state(YTDownloadState.wait_url)
    await message.answer(
        text="Ожидаю ссылку на YouTube видео...",
        reply_markup=CancelKeyboard.build()
    )


@music_yt_router.message(
    F.text[F.regexp(settings.HTTPS_REGEXP)].as_("url"),
    YTDownloadState.wait_url
)
async def download(message: types.Message, state: FSMContext, url: str):
    await state.set_state(YTDownloadState.download)
    service_message = await message.answer(
        text="Начинаю скачивание..."
    )
    audio_io, filename = await set_async(audio.download_audio)(url)
    await service_message.edit_text(
        text="Отправляю файл..."
    )
    audio_file = BufferedInputFile(
        file=audio_io,
        filename=filename
    )
    await message.answer_document(document=audio_file)
    await service_message.delete()
    await music_start(
        message=message,
        state=state
    )


@music_yt_router.message(
    ~(F.text.regexp(settings.HTTPS_REGEXP)),
    YTDownloadState.wait_url
)
async def invalid_link(message: types.Message):
    service_message = await message.answer("Неверный формат ссылки.")
    await asyncio.sleep(2)
    await service_message.delete()
