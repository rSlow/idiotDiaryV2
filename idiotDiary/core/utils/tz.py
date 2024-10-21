import typing
from datetime import tzinfo

from dateutil import tz

tz_utc = tz.gettz("UTC")
tz_local = typing.cast(tzinfo, tz.gettz())
