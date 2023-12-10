import uuid
from io import BytesIO
from typing import BinaryIO

from PIL import Image, ImageOps
from aiogram.types import BufferedInputFile

from common.utils.decorators import set_async


@set_async
def process_image(image_io: BinaryIO):
    quality = 1024
    with Image.open(image_io) as image:
        new_image = ImageOps.fit(
            image=image,
            size=(quality, quality)
        )
    new_image_io = BytesIO()
    new_image.save(
        fp=new_image_io,
        format="jpeg"
    )
    new_image_io.seek(0)
    return new_image_io


@set_async
def get_aiogram_thumbnail(image_io: BytesIO):
    image_io.seek(0)
    return BufferedInputFile(
        file=image_io.read(),
        filename=uuid.uuid4().hex
    )
