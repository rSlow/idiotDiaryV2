from pathlib import Path

from PIL import ImageFont

from idiotDiary.bot.forms.shaurma.render import paths
from idiotDiary.bot.forms.shaurma.render.helpers import create_amount_text
from idiotDiary.bot.forms.shaurma.render.image_context import ImageContext
from idiotDiary.core.utils import dates
from idiotDiary.core.utils.dates import get_now

X = 1080


def render(temp_dir: Path, name: str, transfer_amount: float, **_kw) -> Path:
    with ImageContext(
            template_path=paths.TEMPLATES_DIR / "iphone" / "from_sberbank" / "to_sberbank.png",
            temp_dir=temp_dir
    ) as context:
        draw = context.draw

        # Имя
        draw.text(
            xy=(X / 2, 780),
            text=f"{name}",
            font=ImageFont.truetype(
                font=paths.font_android,
                size=44
            ),
            anchor="mm"
        )

        # Сумма перевода
        draw.text(
            xy=(X / 2, 660),
            text=create_amount_text(transfer_amount),
            font=ImageFont.truetype(
                font=paths.font_android,
                size=84
            ),
            anchor="mm"
        )

        # Время
        draw.text(
            xy=(45, 35),
            text=f"{get_now():{dates.TIME_FORMAT}}",
            font=ImageFont.truetype(
                font=paths.font_android,
                size=32,
            )
        )

    return context.path
