from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from ...main import grade, get_now
from .. import settings

x = 1125
y = 2436


async def tinkoff_tinkoff_phone_iphone(
        name,
        phone_num,
        start_sum,
        transfer_sum,
):
    str_start_sum = grade(f"{start_sum:.2f}".replace(".", ",")) + " ₽"
    str_transfer_sum = grade(f"{transfer_sum}".replace(".", ",")) + " ₽"
    str_end_sum = grade(f"{round(start_sum - transfer_sum, 2):.2f}".replace(".", ",")) + " ₽"

    changing_string = f"{str_start_sum}         {str_end_sum}"
    stroked_font = ImageFont.truetype(
        font=settings.font_iphone_thin,
        size=48
    )
    length_line, _ = stroked_font.getsize(str_start_sum)
    length_full, height_full = stroked_font.getsize(changing_string)
    start_changing_string = x / 2 - length_full / 2

    image_io = BytesIO()
    image = Image.open(
        fp=settings.template_tinkoff_phone_iphone
    )
    draw = ImageDraw.Draw(image)

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
        xy=(x / 2, 1290),
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
    arrow = Image.open("data/resources/layouts/arrow.png")
    arrow_x, arrow_y = arrow.size
    image.paste(
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

    image.save(image_io, "PNG")
    image_io.seek(0)

    return image_io
