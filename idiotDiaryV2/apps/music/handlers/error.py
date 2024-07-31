from aiogram import Router, F, types
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog import DialogManager, ShowMode
from loguru import logger
from yt_dlp.utils import DownloadError

from ..utils.audio import BigDurationError

error_music_router = Router(name="error_music")


@error_music_router.error(
    ExceptionTypeFilter(BigDurationError),
    F.update.event.message.as_("message")
)
async def big_duration_audio_error(_: types.ErrorEvent,
                                   message: types.Message,
                                   dialog_manager: DialogManager,
                                   **__):
    await message.answer("Видео, на которое вы отправили ссылку, идет более 10 минут. По техническим причинам "
                         "на данный момент скачивание аудио более 10 минут невозможно.")
    dialog_manager.show_mode = ShowMode.SEND
    await dialog_manager.done()


@error_music_router.error(
    ExceptionTypeFilter(DownloadError),
    F.update.event.message.as_("message")
)
async def download_error(error: types.ErrorEvent,
                         message: types.Message,
                         dialog_manager: DialogManager):
    logger.exception(error.exception)
    await message.answer(f"Ошибка скачивания видео: <b>{error.exception.args[0]}</b>.")
    dialog_manager.show_mode = ShowMode.SEND
    await dialog_manager.done()
