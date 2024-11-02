import typing
from datetime import tzinfo, time, datetime

from dateutil import tz

DATE_FORMAT = r"%d.%m.%y"
DATE_FORMAT_USER = "ДД.ММ.ГГ"

TIME_FORMAT = r"%H:%M"
TIME_FORMAT_USER = "ЧЧ:ММ"

DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"
DATETIME_FORMAT_USER = f"{DATE_FORMAT_USER} {TIME_FORMAT_USER}"

tz_utc = tz.gettz("UTC")
tz_local = typing.cast(tzinfo, tz.gettz())


def get_now():
    return datetime.now().astimezone(tz=tz_local)


def get_now_isoformat():
    return get_now().isoformat()


def get_timeshift(user_time: time) -> time:
    now = get_now().replace(tzinfo=None)
    td = now - datetime(
        hour=user_time.hour,
        minute=user_time.minute,
        day=now.day,
        month=now.month,
        year=now.year
    )

    all_minutes_shift = _step_round(td.seconds // 60, 15)
    hour_shift = round(all_minutes_shift // 60, 0)
    minutes_shift = round(all_minutes_shift % 60, 0)

    return time(hour=hour_shift, minute=minutes_shift)


def _step_round(number: int, step: int) -> int:
    return step * round(number / step)
