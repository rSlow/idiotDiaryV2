from io import BytesIO
from typing import BinaryIO

from PIL import Image, ImageOps


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
