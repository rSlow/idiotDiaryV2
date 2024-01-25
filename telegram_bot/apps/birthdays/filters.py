import re
from datetime import datetime
from typing import Any, Optional, Literal

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from config import formats


class StrFTimeValidFilter(BaseFilter):
    def __init__(self,
                 field: str,
                 re_format: str,
                 ftime_format: str,
                 method: Optional[Literal['date', 'time']] = None):
        self.field = field
        self.re_format = re_format
        self.ftime_format = ftime_format
        self.method = method

    async def __call__(self,
                       obj: Message | CallbackQuery,
                       raw_state: str | None = None) -> bool | dict[str, Any]:
        if isinstance(obj, Message):
            raw_dt = obj.text
        elif isinstance(obj, CallbackQuery):
            raw_dt = obj.message.text
        else:
            raise TypeError("obj type not in 'Message | CallbackQuery'")

        try:
            str_dt = match.group() if ((match := re.search(self.re_format, raw_dt))
                                       is not None) else ''
            valid_dt = datetime.strptime(str_dt, self.ftime_format)
            if self.method:
                match self.method:
                    case "date":
                        valid_dt = valid_dt.date()
                    case "time":
                        valid_dt = valid_dt.time()
                    case _:
                        raise ValueError("method can be only '.date()' or '.time()'")
            return {self.field: valid_dt}
        except ValueError:
            return False


class StrFTimeNotValidFilter(BaseFilter):
    async def __call__(self,
                       obj: Message | CallbackQuery,
                       raw_state: str | None = None) -> bool:
        return not await super().__call__(
            obj=obj,
            raw_state=raw_state
        )


class TimeValidFilter(StrFTimeValidFilter):
    def __init__(self):
        super().__init__(
            field="valid_time",
            re_format=formats.TIME_RE_FORMAT,
            ftime_format=formats.TIME_FORMAT,
            method="time"
        )


class DateTimeValidFilter(StrFTimeValidFilter):
    def __init__(self):
        super().__init__(
            field="valid_datetime",
            re_format=formats.DATETIME_RE_FORMAT,
            ftime_format=formats.DATETIME_FORMAT
        )


class TimeNotValidFilter(TimeValidFilter, StrFTimeNotValidFilter):
    pass


class DateTimeNotValidFilter(DateTimeValidFilter, StrFTimeNotValidFilter):
    pass
