from PIL import Image, ImageFont

from common.utils.functions import get_now
from .. import settings
from ..image_io_context import ImageIOContext
from ...prepare_data import prepare_tinkoff_sums

X = 1080


def tinkoff_tinkoff_phone_android(name: str,
                                  phone_num: str,
                                  start_sum: int,
                                  transfer_sum: int | float,
                                  **__):
    str_start_sum, str_transfer_sum, str_end_sum, changing_string = prepare_tinkoff_sums(
        start_sum=start_sum,
        transfer_sum=transfer_sum
    )
    stroked_font = ImageFont.truetype(
        font=settings.font_android,
        size=40
    )
    length_line = stroked_font.getlength(str_start_sum)
    length_full = stroked_font.getlength(changing_string)
    start_changing_string = X / 2 - length_full / 2

    with ImageIOContext(settings.template_tinkoff_phone_android) as context:
        draw = context.draw

        # Время
        draw.text(
            xy=(45, 35),
            text=f"{get_now():%H:%M}",
            font=ImageFont.truetype(
                font=settings.font_android,
                size=32,
            )
        )

        # Имя
        draw.text(
            xy=(X / 2, 920),
            text=f"{name}",
            font=ImageFont.truetype(
                font=settings.font_android,
                size=44
            ),
            anchor="mm",
            fill=(52, 51, 46)
        )

        # Номер телефона
        draw.text(
            xy=(X / 2, 1260),
            text=f"{phone_num}",
            font=ImageFont.truetype(
                font=settings.font_android,
                size=44
            ),
            anchor="mm",
            fill=(0, 0, 0)
        )
        # Сумма перевода
        draw.text(
            xy=(X / 2, 760),
            text=f"- {str_transfer_sum}",
            font=ImageFont.truetype(
                font=settings.font_android,
                size=90
            ),
            anchor="mm",
            fill=(246, 247, 249)
        )

        # Изменение суммы
        draw.text(
            xy=(X / 2, 640),
            text=changing_string,
            font=stroked_font,
            anchor="mm",
            fill=(246, 247, 249)
        )

        # Стрелка
        arrow = Image.open(settings.tinkoff_arrow)
        context.image.paste(
            im=arrow,
            box=(529, 631),
            mask=arrow
        )

        draw.line(
            xy=(
                (start_changing_string, 640),
                (start_changing_string + length_line, 640)
            ),
            fill=(246, 247, 249)
        )
    return context.io
