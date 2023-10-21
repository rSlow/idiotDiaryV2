import asyncio
from typing import Any

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

from common.utils.sync_to_async import set_async
from .main import music_start
from .. import settings
from ..keyboards.main import MusicMainKeyboard
from ..keyboards.yt_downloader import TimecodeKeyboard
from ..utils import audio

from common.keyboards.base import CancelKeyboard
from ..FSM.main import MusicState, YTDownloadState

music_yt_router = Router(name="music_yt")


@music_yt_router.message(
    F.text == MusicMainKeyboard.Buttons.download_from_yt,
    MusicState.start
)
async def start_download_audio(message: types.Message, state: FSMContext):
    await state.set_state(YTDownloadState.url)
    await state.update_data(yt_dlp={
        "url": None,
        "timecode": None
    })
    await message.answer(
        text="Ожидаю ссылку на YouTube видео...",
        reply_markup=CancelKeyboard.build()
    )


@music_yt_router.message(
    F.text[F.regexp(settings.HTTPS_REGEXP)].as_("url"),
    YTDownloadState.url
)
async def timecode_video(message: types.Message, state: FSMContext, url: str):
    await state.set_state(YTDownloadState.timecode)
    data = await state.get_data()
    yt_data: dict[str, Any] = data["yt_dlp"]
    yt_data.update(url=url)
    await state.update_data(yt_dlp=yt_data)

    await message.answer(
        text="При необходимости отправьте таймкод в форматах:\n"
             "  - ЧЧ:ММ:СС-ЧЧ:ММ:СС \n"
             "  - ММ:СС-ММ:СС \n"
             "или нажмите кнопку 'Полностью'",
        reply_markup=TimecodeKeyboard.build()
    )


@music_yt_router.message(
    F.text[F.regexp(settings.FULL_TIMECODE_REGEXP)].as_("timecode"),
    YTDownloadState.timecode
)
@music_yt_router.message(
    F.text == TimecodeKeyboard.Buttons.full,
    YTDownloadState.timecode
)
async def download(message: types.Message, state: FSMContext, timecode: str | None = None):
    await state.set_state(YTDownloadState.download)
    url = (await state.get_data()).get("yt_dlp").get("url")
    if url is None:
        raise RuntimeError("url is None")

    if timecode is not None:
        from_time, to_time = timecode.split("-")
    else:
        from_time, to_time = None, None

    service_message = await message.answer(
        text="Начинаю скачивание..."
    )
    audio_io, filename = await set_async(audio.download_audio)(url, from_time, to_time)
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
    YTDownloadState.url
)
async def invalid_link(message: types.Message):
    service_message = await message.answer("Неверный формат ссылки.")
    await asyncio.sleep(2)
    await service_message.delete()
