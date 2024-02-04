import logging
from io import BytesIO

from aiogram import types
from aiogram.types import BufferedInputFile

from common.keyboards.base import CancelKeyboard
from common.utils.functions import get_now


async def send_file(message: types.Message,
                    image_io: BytesIO,
                    from_bank: str,
                    to_bank: str,
                    device: str) -> None:
    photo = BufferedInputFile(
        file=image_io.read(),
        filename=f"{get_now():%d_%m_%y__%H_%M_%S}.PNG"
    )

    await message.answer_document(
        document=photo,
        reply_markup=CancelKeyboard.build()
    )

    logging.info(f"[SCREEN] |{message.from_user.id}| {from_bank}->{to_bank}/{device}")
