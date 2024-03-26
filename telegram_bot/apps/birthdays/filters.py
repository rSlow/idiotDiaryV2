import re
from abc import ABC
from datetime import datetime, date, time
from typing import Optional, Literal

from config import formats


class StrFTimeValidFactory(ABC):
    def __init__(self,
                 field: str,
                 re_format: str,
                 ftime_format: str,
                 method: Optional[Literal['date', 'time']] = None):
        self.field = field
        self.re_format = re_format
        self.ftime_format = ftime_format
        self.method = method

    def __call__(self, text: str) -> date | time | datetime:
        str_dt = match.group() if ((match := re.search(self.re_format, text))
                                   is not None) else ''
        valid_dt = datetime.strptime(str_dt, self.ftime_format)
        if self.method:
            match self.method:
                case "date":
                    valid_dt = valid_dt.date()
                case "time":
                    valid_dt = valid_dt.time()
                case _:
                    raise RuntimeError("method can be only '.date()' or '.time()'")
        return valid_dt


class StrFTimeNotValidFactory(StrFTimeValidFactory, ABC):
    def __call__(self, text: str) -> bool:
        return not super().__call__(text)


class TimeValidFactory(StrFTimeValidFactory):
    def __init__(self):
        super().__init__(
            field="valid_time",
            re_format=formats.TIME_RE_FORMAT,
            ftime_format=formats.TIME_FORMAT,
            method="time"
        )


class DateTimeValidFactory(StrFTimeValidFactory):
    def __init__(self):
        super().__init__(
            field="valid_datetime",
            re_format=formats.DATETIME_RE_FORMAT,
            ftime_format=formats.DATETIME_FORMAT
        )
