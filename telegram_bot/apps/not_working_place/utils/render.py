from .. import settings
from common.jinja import render_template


def render_inn():
    return render_template(
        template_name="inn_parser_message.jinja2",
        templates_dir=settings.TEMPLATES_DIR
    )
