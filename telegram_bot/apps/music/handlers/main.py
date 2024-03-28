from aiogram import Router, F, types
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const
from yt_dlp import DownloadError

from common.buttons import MAIN_MENU_BUTTON
from ..states import MusicMainFSM, YTDownloadFSM, EyeD3FSM
from ..utils.audio import BigDurationError

start_music_dialog = Dialog(
    Window(
        Const("Выберите действие:"),
        Start(
            Const("Редактор eyeD3 👁‍🗨"),
            id="eyed3_editor",
            state=EyeD3FSM.wait_file
        ),
        Start(
            Const("Скачать музыку из видео ⬇️"),
            id="music_download",
            state=YTDownloadFSM.url
        ),
        MAIN_MENU_BUTTON,
        state=MusicMainFSM.state
    )
)

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
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await dialog_manager.done()


@error_music_router.error(
    ExceptionTypeFilter(DownloadError),
    F.update.event.message.as_("message")
)
async def download_error(error: types.ErrorEvent,
                         message: types.Message,
                         dialog_manager: DialogManager):
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.answer(f"Ошибка скачивания видео: <b>{error.exception.args[0]}</b>.")
