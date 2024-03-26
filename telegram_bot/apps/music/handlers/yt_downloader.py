from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from common.filters import regexp_factory
from common.buttons import MAIN_MENU_BUTTON, BACK_BUTTON, CANCEL_BUTTON
from .. import settings
from ..states import YTDownloadFSM
from ..utils import audio


async def valid_link(_: types.Message,
                     __: ManagedTextInput,
                     manager: DialogManager,
                     url: str):
    manager.dialog_data.update({"url": url})
    await manager.next()


async def invalid_link(message: types.Message, *_):
    await message.answer("Неверный формат ссылки.")


async def download(message: types.Message,
                   manager: DialogManager):
    data = manager.dialog_data
    chat_id = message.chat.id
    dialog_message_id: int = manager.current_stack().last_message_id

    url = data.get("url")
    timecode = data.get("timecode")
    if url is None:
        raise RuntimeError("url is None")

    if timecode is not None:
        from_time, to_time = timecode.split("-")
    else:
        from_time, to_time = None, None

    await message.bot.edit_message_text(
        chat_id=chat_id,
        message_id=dialog_message_id,
        text="Начинаю скачивание..."
    )
    audio_io, filename = await audio.download_audio(url, from_time, to_time)
    await message.bot.edit_message_text(
        chat_id=chat_id,
        message_id=dialog_message_id,
        text="Отправляю файл..."
    )
    audio_file = types.BufferedInputFile(
        file=audio_io,
        filename=filename
    )
    await message.answer_document(document=audio_file)

    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


async def full_timecode(callback: types.CallbackQuery,
                        _: Button,
                        manager: DialogManager):
    await download(callback.message, manager)


async def valid_timecode(message: types.Message,
                         __: ManagedTextInput,
                         manager: DialogManager,
                         timecode: str):
    await message.delete()
    manager.dialog_data.update({"timecode": timecode})
    await download(message, manager)


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
        Const("При необходимости отправьте таймкод в форматах:"),
        Const("  - ЧЧ:ММ:СС-ЧЧ:ММ:СС"),
        Const("  - ММ:СС-ММ:СС"),
        Const("или нажмите кнопку 'Полностью'"),
        Button(
            Const("Полностью"),
            id="full",
            on_click=full_timecode
        ),
        TextInput(
            id="timecode",
            type_factory=regexp_factory(settings.FULL_TIMECODE_REGEXP),
            on_success=valid_timecode,
            on_error=invalid_timecode
        ),
        BACK_BUTTON,
        MAIN_MENU_BUTTON,
        state=YTDownloadFSM.timecode
    )
)
