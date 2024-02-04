from datetime import date
from typing import Sequence

from common.jinja import render_template
from .. import settings as birthdays_settings
from ..ORM.birthdays import Birthday
from ..ORM.notifications import NotificationTime


def render_check_birthdays(dates: dict[date, Sequence[Birthday]]) -> str:
    return render_template(
        template_name="day_birthdays.jinja2",
        data={"dates": dates},
        templates_dir=birthdays_settings.TEMPLATES_DIR
    )


def render_schedule_birthdays(today: date,
                              tomorrow: date,
                              today_birthdays: Sequence[Birthday],
                              tomorrow_birthdays: Sequence[Birthday]) -> str:
    return render_template(
        template_name="schedule_birthdays.jinja2",
        data={
            "today": today,
            "tomorrow": tomorrow,
            "today_birthdays": today_birthdays,
            "tomorrow_birthdays": tomorrow_birthdays
        },
        templates_dir=birthdays_settings.TEMPLATES_DIR
    )


def render_notifications(notifications: Sequence[NotificationTime]) -> str:
    times = [notification.time for notification in notifications]
    return render_template(
        template_name="notifications.jinja2",
        data={"times": times},
        templates_dir=birthdays_settings.TEMPLATES_DIR
    )


def render_time_correction() -> str:
    return render_template(
        template_name="time_correction.jinja2",
        templates_dir=birthdays_settings.TEMPLATES_DIR
    )
