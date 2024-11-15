from pathlib import Path

from aiofiles import tempfile as atf
from aiogram import types, Bot
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from taskiq import AsyncTaskiqTask, TaskiqResult

from idiotDiary.bot.states.not_working_place import ImagesZipSG
from idiotDiary.bot.views import buttons as b
from idiotDiary.core.config import Paths
from idiotDiary.mq.tasks.zip import zip_files_in_folder

DD_KEY = "photos"


async def photos_count_getter(dialog_manager: DialogManager, **__):
    photo_list = dialog_manager.dialog_data.get(DD_KEY, [])
    return {"count": len(photo_list)}


async def photo_handler(message: types.Message, _, manager: DialogManager):
    manager.dialog_data.setdefault(DD_KEY, []).append(message.photo[-1].file_id)
    await message.delete()


@inject
async def send_photos(
        callback: types.CallbackQuery, _, manager: DialogManager,
        paths: FromDishka[Paths], bot: FromDishka[Bot]
):
    file_id_list = manager.dialog_data.get(DD_KEY)
    await callback.message.edit_text(
        f"Запаковывается {len(file_id_list)} фотографий..."
    )
    async with atf.TemporaryDirectory(dir=paths.temp_folder_path) as temp_dir:
        temp_path = Path(temp_dir)
        for i, file_id in enumerate(file_id_list, 1):
            await bot.download(file_id, temp_path / f"{i}.jpg")
        task: AsyncTaskiqTask = await zip_files_in_folder.kiq(temp_path)
        zip_file_path: TaskiqResult = await task.wait_result(timeout=60)
        print(zip_file_path.return_value)
        zip_doc = types.FSInputFile(zip_file_path.return_value)
        await callback.message.edit_text("Архив отправляется...")
        await callback.message.answer_document(zip_doc)

    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


zip_photos_dialog = Dialog(
    Window(
        Const("Жду фотографий. Как отправлены все - нажать <b>Запаковать!</b>"),
        Button(
            Format("Запаковать {count} фотографий!"),
            when="count",
            on_click=send_photos,  # noqa
            id="send_photos"
        ),
        MessageInput(
            func=photo_handler,
            content_types=ContentType.PHOTO
        ),
        b.CANCEL,
        getter=photos_count_getter,
        state=ImagesZipSG.state
    )
)