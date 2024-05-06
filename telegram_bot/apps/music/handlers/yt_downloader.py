from datetime import datetime
from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from common.filters import regexp_factory
from common.buttons import MAIN_MENU_BUTTON, BACK_BUTTON, CANCEL_BUTTON
from common.utils.functions import edit_dialog_message
from .. import settings
from ..states import YTDownloadFSM
from ..utils.audio import download_audio


async def valid_link(_: types.Message,
                     __: ManagedTextInput,
                     manager: DialogManager,
                     url: str):
    manager.dialog_data.update({"url": url})
    await manager.next()


async def invalid_link(message: types.Message, *_):
    await message.answer("Неверный формат ссылки.")


async def download_and_send_file(message: types.Message,
                                 manager: DialogManager):
    data = manager.dialog_data
    url = data.get("url")
    timecode = data.get("timecode")

    if url is None:
        raise RuntimeError("url is None")

    if timecode is not None:
        string_from_time, string_to_time = timecode.split("-")
        from_time = datetime.strptime(string_from_time, settings.STRFTIME_FORMAT)
        to_time = datetime.strptime(string_to_time, settings.STRFTIME_FORMAT)
    else:
        from_time, to_time = None, None

    await edit_dialog_message(
        manager=manager,
        text="Начинаю скачивание..."
    )
    result = await download_audio(
        url=url,
        root_temp_path=settings.TEMP_DIR,
        from_time=from_time,
        to_time=to_time
    )
    await edit_dialog_message(
        manager=manager,
        text="Отправляю файл..."
    )
    audio_file = types.BufferedInputFile(
        file=result.data,
        filename=result.filename
    )
    await message.answer_document(document=audio_file)

    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


async def full_timecode(callback: types.CallbackQuery,
                        _: Button,
                        manager: DialogManager):
    await download_and_send_file(callback.message, manager)


async def valid_timecode(message: types.Message,
                         __: ManagedTextInput,
                         manager: DialogManager,
                         timecode: str):
    await message.delete()
    manager.dialog_data.update({"timecode": timecode})
    await download_and_send_file(message, manager)


async def invalid_timecode(message: types.Message, *_):
    await message.answer("Неверный формат таймкода.")


music_yt_dialog = Dialog(
    Window(
        Const("Ожидаю ссылку на YouTube видео..."),
        TextInput(
            id="url",
            on_success=valid_link,
            on_error=invalid_link,
            type_factory=regexp_factory(settings.HTTPS_REGEXP)
        ),
        CANCEL_BUTTON,
        state=YTDownloadFSM.url
    ),
    Window(
        Const("При необходимости отправьте таймкод в формате: ЧЧ:ММ:СС-ЧЧ:ММ:СС"),
        Const("или нажмите кнопку 'Полностью'"),
        Button(
            Const("Полностью"),
            id="full",
            on_click=full_timecode
        ),
        TextInput(
            id="timecode",
            type_factory=regexp_factory(settings.PAIR_TIMECODE_REGEXP),
            on_success=valid_timecode,
            on_error=invalid_timecode
        ),
        BACK_BUTTON,
        MAIN_MENU_BUTTON,
        state=YTDownloadFSM.timecode
    )
)
