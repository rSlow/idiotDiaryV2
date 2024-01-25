from datetime import datetime, time, timedelta

from common.utils.functions import get_now


def get_timeshift(user_datetime: datetime):
    now = get_now().replace(tzinfo=None)
    td = now - user_datetime

    all_minutes_shift = step_round(td.seconds // 60, 15)
    hour_shift = round(all_minutes_shift // 60, 0)
    minutes_shift = round(all_minutes_shift % 60, 0)

    return time(
        hour=hour_shift,
        minute=minutes_shift
    )


def step_round(number: int, step: int):
    return step * round(number / step)
