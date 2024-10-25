import itertools
import tempfile
from dataclasses import dataclass
from pathlib import Path

import aiofiles.tempfile
from aiogram import types, Bot, F
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from apps.not_working_place.settings import APP_TEMP_ROOT
from apps.not_working_place.states import ZipPdfFSM
from common.buttons import CANCEL_BUTTON
from PyPDF2 import PdfWriter, PdfReader, PageObject

DD_KEY = "files"


@dataclass
class File:
    file_id: str
    filename: str


async def file_handler(message: types.Message,
                       _: MessageInput,
                       manager: DialogManager):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    document = message.document

    files: list[File] = manager.dialog_data.setdefault(DD_KEY, [])
    file = File(
        file_id=document.file_id,
        filename=document.file_name
    )
    files.append(file)


async def on_zip_ready(callback: types.CallbackQuery,
                       _: Button,
                       manager: DialogManager):
    bot: Bot = manager.middleware_data["bot"]
    message = callback.message
    files: list[File] = manager.dialog_data.get(DD_KEY, [])

    await message.edit_text(text="Обработка...")

    async with aiofiles.tempfile.TemporaryDirectory(dir=APP_TEMP_ROOT) as tmp:
        temp_dir = Path(tmp)
        for file_id in files:
            await bot.download(
                file=file_id.file_id,
                destination=temp_dir / file_id.filename
            )

        page_lists: list[list[PageObject]] = []
        for file in temp_dir.glob("*.*"):
            page_lists.append(PdfReader(file).pages)

        max_pages: int = len(max(page_lists, key=lambda x: len(x)))
        page_cycles: list[itertools.islice[PageObject]] = [
            itertools.islice(itertools.cycle(iterable), max_pages)
            for iterable in page_lists
        ]
        writer = PdfWriter()
        page_groups = zip(*page_cycles)
        for page_group in page_groups:
            for page in page_group:
                writer.add_page(page)

        with tempfile.TemporaryFile(mode="rb") as result_file:
            writer.write(result_file)
            pdf_document = types.BufferedInputFile(
                file=result_file.read(),
                filename=files[0].filename
            )
            await message.answer_document(document=pdf_document)

    await manager.done()


async def getter(dialog_manager: DialogManager):
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
            id="zip",
            # when=WhenDialogKey(DD_KEY),
            when=F.dialog_manager.dialog_data[DD_KEY],
            on_click=on_zip_ready
        ),
        CANCEL_BUTTON,
        state=ZipPdfFSM.state
    )
)
