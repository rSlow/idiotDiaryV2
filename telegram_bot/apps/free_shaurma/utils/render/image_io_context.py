from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw


@dataclass
class EnterContext:
    draw: ImageDraw.Draw
    io: BytesIO
    image: Image


class ImageIOContext:
    def __init__(self, template_path: Path):
        self.template_path = template_path
        self.image_io = BytesIO()
        self.image: Optional[Image] = None

    def __enter__(self):
        self.image = Image.open(
            fp=self.template_path
        )
        draw = ImageDraw.Draw(self.image)
        return EnterContext(
            draw=draw,
            io=self.image_io,
            image=self.image
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.image.save(self.image_io, "PNG")
        self.image_io.seek(0)
