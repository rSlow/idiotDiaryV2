from pathlib import Path

from PIL import ImageFont, Image

from idiotDiary.bot.forms.shaurma.render import paths
from idiotDiary.bot.forms.shaurma.render.helpers import create_amount_text
from idiotDiary.bot.forms.shaurma.render.image_context import ImageContext
from idiotDiary.core.utils import dates
from idiotDiary.core.utils.dates import get_now

X = 1080


def render(
        temp_dir: Path, name: str, phone_num: str,
        start_amount: int, transfer_amount: int | float,
        **_kw
) -> Path:
    str_start_amount = create_amount_text(start_amount)
    str_end_amount = create_amount_text(start_amount - transfer_amount)
    changing_string = f"{str_start_amount}         {str_end_amount}"

    stroked_font = ImageFont.truetype(font=paths.font_android, size=40)
    length_full = stroked_font.getlength(changing_string)
    start_changing_string = X / 2 - length_full / 2
    length_line = stroked_font.getlength(str_start_amount)

    with ImageContext(
            template_path=paths.TEMPLATES_DIR / "android" / "from_tinkoff" / "to_tinkoff.png",
            temp_dir=temp_dir
    ) as context:
        draw = context.draw

        # Время
        draw.text(
            xy=(45, 35),
            text=f"{get_now():{dates.TIME_FORMAT}}",
            font=ImageFont.truetype(
                font=paths.font_android,
                size=32,
            )
        )

        # Имя
        draw.text(
            xy=(X / 2, 920),
            text=f"{name}",
            font=ImageFont.truetype(
                font=paths.font_android,
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
                font=paths.font_android,
                size=44
            ),
            anchor="mm",
            fill=(0, 0, 0)
        )
        # Сумма перевода
        draw.text(
            xy=(X / 2, 760),
            text=f"- {create_amount_text(transfer_amount)}",
            font=ImageFont.truetype(
                font=paths.font_android,
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
        arrow = Image.open(paths.LAYOUTS_DIR / "arrow.png")
        context.image.paste(
            im=arrow,
            box=(529, 631),
            mask=arrow
        )

        # Линия зачеркивающая стартовую сумму
        draw.line(
            xy=(
                (start_changing_string, 640),
                (start_changing_string + length_line, 640)
            ),
            fill=(246, 247, 249)
        )

    return context.path
