import logging

from aiogram import types
from io import BytesIO

from aiogram.types import BufferedInputFile

from ..utils.main import get_now
from common.base_keyboard import CancelKeyboard


async def send_file(message: types.Message,
                    image_io: BytesIO,
                    bank,
                    on_bank,
                    device):
    photo = BufferedInputFile(
        file=image_io.read(),
        filename=f"{get_now():%d_%m_%y__%H_%M_%S}.PNG"
    )

    await message.answer_document(
        document=photo,
        reply_markup=CancelKeyboard.build()
    )

    logging.info(f"[SCREEN] |{message.from_user.id}| {bank}->{on_bank}/{device}")
