import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw
from PIL.ImageFile import ImageFile


@dataclass
class EnterContext:
    draw: ImageDraw
    image: ImageFile
    path: Path


class ImageContext:
    def __init__(self, template_path: Path, temp_dir: Path):
        self.template_path = template_path

        self._ext: str = "png"
        self.file_path = temp_dir / f"{uuid.uuid4().hex}.{self._ext}"

        self.image: Optional[ImageFile] = None

    def __enter__(self):
        self.image = Image.open(fp=self.template_path)
        draw = ImageDraw.Draw(self.image)
        return EnterContext(draw=draw, path=self.file_path, image=self.image)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.image.save(self.file_path, "png")
