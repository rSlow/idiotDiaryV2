from PIL import ImageFont

from common.utils.functions import get_now
from .. import settings
from ..image_io_context import ImageIOContext
from ...main import grade

X = 1080


def sberbank_sberbank_phone_android(name: int,
                                    transfer_sum: int | float,
                                    **__):
    str_transfer_sum = f"{transfer_sum}".replace(".", ",")

    with ImageIOContext(settings.template_sberbank_android) as context:
        draw = context.draw

        # Имя
        draw.text(
            xy=(X / 2, 780),
            text=f"{name}",
            font=ImageFont.truetype(
                font=settings.font_android,
                size=44
            ),
            anchor="mm"
        )

        # Сумма перевода
        draw.text(
            xy=(X / 2, 660),
            text=f"{grade(str_transfer_sum)} ₽",
            font=ImageFont.truetype(
                font=settings.font_android,
                size=84
            ),
            anchor="mm"
        )

        # Время
        draw.text(
            xy=(45, 35),
            text=f"{get_now():%H:%M}",
            font=ImageFont.truetype(
                font=settings.font_android,
                size=32,
            )
        )

    return context.io
