import asyncio
from dataclasses import dataclass
from pathlib import Path

import aiofiles.tempfile as atf
from adaptix import Retort
from aiogram import types, F, Bot
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from taskiq import AsyncTaskiqTask, TaskiqResult, TaskiqResultTimeoutError

from idiotDiary.bot.states.not_working_place import ZipPdfSG
from idiotDiary.bot.views import buttons as b
from idiotDiary.core.config import Paths
from idiotDiary.core.utils.exceptions.taskiq import TaskiqTaskError
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
        paths: FromDishka[Paths], bot: FromDishka[Bot]
):
    message = callback.message
    files_data = manager.dialog_data.get(DD_KEY, [])
    files = [file_retort.load(file_data, File) for file_data in files_data]
    await message.edit_text(text="Обработка...")

    try:
        async with atf.TemporaryDirectory(dir=paths.temp_folder_path) as tmp:
            temp_dir = Path(tmp)
            file_paths: list[Path] = []
            for file in files:
                file_path = temp_dir / file.filename
                file_paths.append(file_path)
                await bot.download(
                    file=file.file_id,
                    destination=file_path
                )
                await asyncio.sleep(0.1)  # flood control

            task: AsyncTaskiqTask = await pack_pdf_file.kiq(file_paths)
            zip_pdf_result: TaskiqResult = await task.wait_result(timeout=120)
            if error := zip_pdf_result.error:
                await message.answer(
                    "Произошла ошибка генерации PDF. Задача отменена."
                )
                raise TaskiqTaskError("Ошибка генерации PDF файла:", error)

            pdf_file = types.FSInputFile(zip_pdf_result.return_value)
            await callback.message.answer_document(pdf_file)

    except TaskiqResultTimeoutError:
        await message.answer("Тайм-аут запроса. Задача отменена.")

    finally:
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
