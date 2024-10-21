from typing import Any

from common.jinja import render_template
from .. import settings


def render_eyed3(eyed3_data: dict[str, Any]):
    return render_template(
        template_name="eyed3_data.jinja2",
        data=eyed3_data,
        templates_dir=settings.TEMPLATES_DIR
    )
