from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from common.utils.functions import get_now
from .. import settings
from ...main import grade


def sberbank_sberbank_phone_android(
        name,
        transfer_sum,
):
    str_transfer_sum = f"{transfer_sum}".replace(".", ",")

    image_io = BytesIO()
    image = Image.open(
        fp=settings.template_sberbank_android
    )
    draw = ImageDraw.Draw(image)

    # Имя
    draw.text(
        xy=(540, 780),
        text=f"{name}",
        font=ImageFont.truetype(
            font=settings.font_android,
            size=44
        ),
        anchor="mm"
    )

    # Сумма перевода
    draw.text(
        xy=(540, 660),
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

    image.save(image_io, "PNG")
    image_io.seek(0)

    return image_io
