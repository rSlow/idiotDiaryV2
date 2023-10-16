from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from .. import settings
from ...main import grade, get_now

x = 1170
y = 2532


async def sberbank_sberbank_phone_iphone(
        name,
        transfer_sum,
):
    str_transfer_sum = f"{transfer_sum}".replace(".", ",")

    image_io = BytesIO()
    image = Image.open(
        fp=settings.template_sberbank_iphone
    )
    draw = ImageDraw.Draw(image)

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

    image.save(image_io, "PNG")
    image_io.seek(0)

    return image_io
