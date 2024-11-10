from PIL import ImageFont
from PIL.ImageDraw import ImageDraw

from common.utils.functions import get_now
from .. import settings
from ..image_io_context import ImageIOContext
from ...main import grade

X = 828


def sberbank_sberbank_phone_iphone(name: str,
                                   transfer_sum: int | float,
                                   **__):
    str_transfer_sum = f"{transfer_sum}".replace(".", ",")

    with ImageIOContext(settings.template_sberbank_iphone) as context:
        draw: ImageDraw = context.draw

    return context.io
