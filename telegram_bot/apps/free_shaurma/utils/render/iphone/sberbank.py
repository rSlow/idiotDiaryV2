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
        # Имя
        draw.text(
            xy=(X / 2, 1042),
            text=f"{name}",
            font=ImageFont.truetype(
                font=settings.font_iphone_medium,
                size=30
            ),
            anchor="mm",
            fill=(119, 119, 119)
        )

        # Сумма перевода
        draw.text(
            xy=(X / 2, 922),
            text=f"{grade(str_transfer_sum)} ₽",
            font=ImageFont.truetype(
                font=settings.font_iphone_bold,
                size=66
            ),
            anchor="mm",
            fill=(0, 0, 0)
        )

        # Время
        draw.text(
            xy=(35, 29),
            text=f"{get_now():%H:%M}",
            font=ImageFont.truetype(
                font=settings.font_iphone_bold,
                size=34,
            ),
            fill=(0, 0, 0)
        )

    return context.io
