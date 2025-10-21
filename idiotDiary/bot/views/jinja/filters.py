from datetime import datetime, timedelta

from idiotDiary.core.utils import dates


def datetime_filter(
        value: datetime | None, format_: str = dates.DATETIME_FORMAT
) -> str:
    if value is None:
        return "n/a"
    return value.strftime(format_)


def timedelta_filter(value: timedelta) -> str:
    minutes = value.seconds // 60
    return f"{minutes} мин."


def declension_filter(value: int) -> str:
    if value % 10 == 1 and value != 11:
        return "год"
    elif value % 10 in [2, 3, 4] and (value < 10 or value > 20):
        return "года"
    return "лет"
