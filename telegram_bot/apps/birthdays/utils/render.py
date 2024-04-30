from datetime import date
from typing import Sequence

from common.jinja import render_template
from .. import settings as birthdays_settings
from ..ORM.birthdays import Birthday


def render_check_birthdays(dates: dict[date, Sequence[Birthday]]) -> str:
    return render_template(
        template_name="day_birthdays.jinja2",
        data={"dates": dates},
        templates_dir=birthdays_settings.TEMPLATES_DIR
    )


def render_schedule_birthdays(today_birthdays: Sequence[Birthday],
                              tomorrow_birthdays: Sequence[Birthday]) -> str:
    return render_template(
        template_name="schedule_birthdays.jinja2",
        data={
            "today_birthdays": today_birthdays,
            "tomorrow_birthdays": tomorrow_birthdays
        },
        templates_dir=birthdays_settings.TEMPLATES_DIR
    )
