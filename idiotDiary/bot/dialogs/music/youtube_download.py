from datetime import datetime
from pathlib import Path

from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from idiotDiary.bot.states.music import YTDownloadSG
from idiotDiary.bot.utils.message import edit_dialog_message
from idiotDiary.bot.utils.taskiq_context import TaskiqContext
from idiotDiary.bot.utils.type_factory import regexp_factory, HTTPS_REGEXP, PAIR_TIMECODE_REGEXP
from idiotDiary.bot.views import buttons as b
from idiotDiary.mq.tasks.music import download_youtube_audio


async def valid_link(_, __, manager: DialogManager, url: str):
    manager.dialog_data.update({"url": url})
    await manager.next()


async def invalid_link(message: types.Message, _, __, ___):
    await message.answer("Неверный формат ссылки.")


url_window = Window(
    Const("Ожидаю ссылку на YouTube видео..."),
    TextInput(
        id="url",
        on_success=valid_link,
        on_error=invalid_link,
        type_factory=regexp_factory(HTTPS_REGEXP)
    ),
    b.CANCEL,
    state=YTDownloadSG.url
)


async def full_timecode(callback: types.CallbackQuery, _, manager: DialogManager):
    await download_and_send_file(callback.message, manager)


async def valid_timecode(message: types.Message, _, manager: DialogManager, timecode: str):
    await message.delete()
    manager.dialog_data.update({"timecode": timecode})
    await download_and_send_file(message, manager)


async def invalid_timecode(message: types.Message, *_):
    await message.answer("Неверный формат таймкода.")


async def download_and_send_file(message: types.Message, manager: DialogManager):
    await edit_dialog_message(manager=manager, text="Начинаю скачивание...")

    url = manager.dialog_data.get("url")
    if url is None:
        raise RuntimeError("`url` is None")  # TODO

    timecode: str | None = manager.dialog_data.get("timecode")
    if timecode is not None:
        str_from_time, str_to_time = timecode.split("-", maxsplit=1)
        from_time = datetime.strptime(str_from_time, r"%H:%M:%S")
        to_time = datetime.strptime(str_to_time, r"%H:%M:%S")
    else:
        from_time, to_time = None, None

    async with TaskiqContext(
            task=download_youtube_audio, manager=manager,
            error_log_message="Ошибка скачивания аудио",
            error_user_message="Произошла ошибка скачивания файла. Загрузка отменена.",
            timeout_message="Превышено время скачивания видео.",
    ) as context:
        audio_file_path: Path = await context.wait_result(
            timeout=120, temp_path=context.temp_folder,
            url=url, from_time=from_time, to_time=to_time
        )
        await edit_dialog_message(manager=manager, text="Отправляю файл...")
        audio_file = types.FSInputFile(path=audio_file_path)
        await message.answer_document(document=audio_file)

    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


timecode_window = Window(
    Const("При необходимости отправьте таймкод в формате: ЧЧ:ММ:СС-ЧЧ:ММ:СС"),
    Const("или нажмите кнопку 'Полностью'"),
    Button(
        Const("Полностью"),
        id="full",
        on_click=full_timecode
    ),
    TextInput(
        id="timecode",
        type_factory=regexp_factory(PAIR_TIMECODE_REGEXP),
        on_success=valid_timecode,
        on_error=invalid_timecode
    ),
    b.BACK,
    b.MAIN_MENU,
    state=YTDownloadSG.timecode
)

download_audio_dialog = Dialog(
    url_window,
    timecode_window,
)
