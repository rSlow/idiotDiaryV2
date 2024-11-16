import asyncio
from dataclasses import dataclass
from pathlib import Path

from adaptix import Retort
from aiogram import types, F, Bot
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from idiotDiary.bot.states.not_working_place import ZipPdfSG
from idiotDiary.bot.utils.taskiq_context import TaskiqContext
from idiotDiary.bot.views import buttons as b
from idiotDiary.mq.tasks.pdf import pack_pdf_file

DD_KEY = "files"


@dataclass
class File:
    file_id: str
    filename: str


file_retort = Retort()


async def file_handler(message: types.Message, _, manager: DialogManager):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    document = message.document

    files = manager.dialog_data.setdefault(DD_KEY, [])
    files.append({
        "file_id": document.file_id,
        "filename": document.file_name
    })


@inject
async def on_zip_ready(
        callback: types.CallbackQuery, _, manager: DialogManager,
        bot: FromDishka[Bot]
):
    message = callback.message
    files_data = manager.dialog_data.get(DD_KEY, [])
    files = [file_retort.load(file_data, File) for file_data in files_data]
    await message.edit_text(text="Обработка...")

    async with TaskiqContext(
            task=pack_pdf_file, manager=manager,
            error_log_message="Ошибка генерации PDF файла:",
            error_user_message="Произошла ошибка генерации PDF. "
                               "Задача отменена.",
            timeout_message="Тайм-аут запроса. Задача отменена.",
    ) as context:
        file_paths: list[Path] = []
        for file in files:
            file_path = context.temp_folder / file.filename
            file_paths.append(file_path)
            await bot.download(file=file.file_id, destination=file_path)
            await asyncio.sleep(0.1)  # flood control
        pdf_file_path: Path = await context.wait_result(
            timeout=120, file_paths=file_paths
        )
        pdf_file = types.FSInputFile(pdf_file_path)
        await callback.message.answer_document(pdf_file)

    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


async def getter(dialog_manager: DialogManager, **__):
    return {"files_count": len(dialog_manager.dialog_data.get(DD_KEY, []))}


zip_pdf_dialog = Dialog(
    Window(
        Const("Ожидаю PDF файлы..."),
        MessageInput(
            func=file_handler,
            content_types=[ContentType.DOCUMENT]
        ),
        Button(
            text=Format("Склеить {files_count} файл(ов)"),
            when=F["files_count"] > 0,
            id="run_zip",
            on_click=on_zip_ready  # noqa
        ),
        b.CANCEL,
        getter=getter,
        state=ZipPdfSG.state
    )
)
