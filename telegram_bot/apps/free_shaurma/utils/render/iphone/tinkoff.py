from PIL import Image, ImageFont

from common.utils.functions import get_now
from .. import settings
from ..image_io_context import ImageIOContext
from ...prepare_data import prepare_tinkoff_sums

x = 1125
y = 2436


def tinkoff_tinkoff_phone_iphone(name: str,
                                 phone_num: str,
                                 start_sum: int | float,
                                 transfer_sum: int | float,
                                 **__):
    str_start_sum, str_transfer_sum, str_end_sum, changing_string = prepare_tinkoff_sums(
        start_sum=start_sum,
        transfer_sum=transfer_sum
    )
    stroked_font = ImageFont.truetype(
        font=settings.font_iphone_thin,
        size=48
    )
    length_line = stroked_font.getlength(str_start_sum)
    length_full = stroked_font.getlength(changing_string)
    start_changing_string = x / 2 - length_full / 2

    with ImageIOContext(settings.template_tinkoff_phone_iphone) as context:
        draw = context.draw

        # Время
        draw.text(
            xy=(68, 43),
            text=f"{get_now():%H:%M}",
            font=ImageFont.truetype(
                font=settings.font_iphone_bold,
                size=44,
            )
        )

        # Имя
        draw.text(
            xy=(x / 2, 935),
            text=f"{name}",
            font=ImageFont.truetype(
                font=settings.font_iphone_thin,
                size=50,
                index=0
            ),
            anchor="mm",
            fill=(51, 51, 51)
        )

        # Номер телефона
        draw.text(
            xy=(x / 2, 1300),
            text=f"{phone_num}",
            font=ImageFont.truetype(
                font=settings.font_iphone_thin,
                size=50
            ),
            anchor="mm",
            fill=(51, 51, 51)
        )

        # Сумма перевода
        draw.text(
            xy=(x / 2, 760),
            text=f"- {str_transfer_sum}",
            font=ImageFont.truetype(
                font=settings.font_iphone_bold,
                size=100
            ),
            anchor="mm",
            fill=(246, 247, 249)
        )

        # Изменение суммы
        draw.text(
            xy=(x / 2, 630),
            text=changing_string,
            font=stroked_font,
            anchor="mm",
            fill=(246, 247, 249)
        )

        # Стрелка
        arrow = Image.open(settings.tinkoff_arrow)
        arrow_x, arrow_y = arrow.size
        context.image.paste(
            im=arrow,
            box=(int(x / 2), int(630 - arrow_y / 2)),
            mask=arrow
        )

        draw.line(
            xy=(
                (start_changing_string, 630),
                (start_changing_string + length_line, 630)
            ),
            fill=(246, 247, 249)
        )

    return context.io
