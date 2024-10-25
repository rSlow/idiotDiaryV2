from aiogram import types
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.api.entities import Context
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from common.buttons import CANCEL_BUTTON
from ..states import ImagesZipFSM
from ..utils import photos

DD_KEY = "PHOTOS"


async def photos_count_getter(aiogd_context: Context, **__):
    photo_list = aiogd_context.dialog_data.get(DD_KEY, [])
    return {"count": len(photo_list)}


async def photo_handler(message: types.Message,
                        _: MessageInput,
                        manager: DialogManager) -> None:
    manager.show_mode = ShowMode.EDIT
    manager.dialog_data.setdefault(DD_KEY, []).append(message.photo[-1].file_id)
    await message.delete()


async def send_photos(callback: types.CallbackQuery,
                      _: Button,
                      manager: DialogManager):
    file_id_list = manager.dialog_data.get(DD_KEY)
    await callback.message.edit_text(f"Запаковывается {len(file_id_list)} фотографий...")
    zip_file = await photos.get_zip_file(file_id_list, bot=callback.bot)
    await callback.message.edit_text("Архив отправляется...")
    await callback.message.answer_document(zip_file)
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


pack_dialog = Dialog(
    Window(
        Const("Жду фотографий. Как отправлены все - нажать <b>Запаковать!</b>"),
        Button(
            Format("Запаковать {count} фотографий!"),
            when="count",
            on_click=send_photos,
            id="send_photos"
        ),
        MessageInput(
            func=photo_handler,
            content_types=ContentType.PHOTO
        ),
        CANCEL_BUTTON,
        getter=photos_count_getter,
        state=ImagesZipFSM.state
    )
)
