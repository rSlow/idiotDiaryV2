import re
from os import PathLike
from typing import Sequence

from jinja2 import Environment, FileSystemLoader

from config import settings, formats
from .utils.functions import get_now

PATH_TYPE = str | PathLike | Sequence[str | PathLike]


def render_template(
        template_name: str,
        data: dict | None = None,
        templates_dir: PATH_TYPE | None = None
) -> str:
    if data is None:
        context = {}
    else:
        context = data.copy()
    context.update(get_context())

    env = Environment(
        loader=FileSystemLoader(searchpath=templates_dir or settings.TEMPLATES_DIR),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True
    )

    template = env.get_template(template_name)
    rendered = template.render(**context)
    rendered = rendered.replace("\n", " ")
    rendered = rendered.replace("<br>", "\n")
    rendered = re.sub(" +", " ", rendered).replace(" .", ".").replace(" ,", ",")
    rendered = "\n".join(line.strip() for line in rendered.split("\n"))

    return rendered


def get_context():
    return {
        "TIME_FORMAT": formats.TIME_FORMAT,
        "TIME_STRING_FORMAT": formats.TIME_STRING_FORMAT,
        "DATE_FORMAT": formats.DATE_FORMAT,
        "DATE_STRING_FORMAT": formats.DATE_STRING_FORMAT,
        "DATETIME_FORMAT": formats.DATETIME_FORMAT,
        "DATETIME_STRING_FORMAT": formats.DATETIME_STRING_FORMAT,
        "now": get_now(),
    }
