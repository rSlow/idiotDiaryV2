from PIL import ImageFont

from common.utils.functions import get_now
from .. import settings
from ..image_io_context import ImageIOContext
from ...main import grade

x = 1170
y = 2532


def sberbank_sberbank_phone_iphone(name: str,
                                   transfer_sum: int | float):
    str_transfer_sum = f"{transfer_sum}".replace(".", ",")

    with ImageIOContext(settings.template_sberbank_iphone) as context:
        draw = context.draw
        # Имя
        draw.text(
            xy=(x / 2, 830),
            text=f"{name}",
            font=ImageFont.truetype(
                font=settings.font_iphone_thin,
                size=40
            ),
            anchor="mm"
        )

        # Сумма перевода
        draw.text(
            xy=(x / 2, 710),
            text=f"{grade(str_transfer_sum)} ₽",
            font=ImageFont.truetype(
                font=settings.font_iphone_bold,
                size=90
            ),
            anchor="mm"
        )

        # Время
        draw.text(
            xy=(60, 45),
            text=f"{get_now():%H:%M}",
            font=ImageFont.truetype(
                font=settings.font_iphone_bold,
                size=48,
            )
        )

    return context.io
