from io import BytesIO

from aiogram import types, Bot
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from apps.not_working_place.states import StickersFSM
from common.buttons import CANCEL_BUTTON
from PIL import Image


async def image_handler(message: types.Message,
                        _: MessageInput,
                        manager: DialogManager):
    if photos := message.photo:
        file_id = photos[-1].file_id
    elif document := message.document:
        file_id = document.file_id
    else:
        return await message.answer("Не было получено нужного объекта.")

    await message.delete()
    manager.show_mode = ShowMode.DELETE_AND_SEND
    bot: Bot = manager.middleware_data["bot"]

    file_io = await bot.download(
        file=file_id,
        destination=BytesIO(),
    )
    with Image.open(file_io) as image:
        image_size = image.size
        new_image_size = get_new_image_size(
            size=image_size,
            max_size=512
        )
        image.resize(new_image_size)

        image_io = BytesIO()
        image.save(image_io)

    image_io.seek(0)
    image_file = types.BufferedInputFile(
        file=image_io.read(),
        filename=f"sticker {file_id}"
    )
    await message.answer_document(document=image_file)


def get_new_image_size(size: tuple[int, int],
                       max_size: int) -> tuple[float, float]:
    x, y = size
    if x > y or x == y:
        offset = x / max_size
    else:
        offset = y / max_size
    return x * offset, y * offset


stickers_dialog = Dialog(
    Window(
        Const("Ожидаю картинку в формате PNG, JPG или BMP..."),
        MessageInput(
            func=image_handler,
            content_types=[ContentType.PHOTO, ContentType.DOCUMENT]
        ),
        CANCEL_BUTTON,
        state=StickersFSM.state
    )
)
