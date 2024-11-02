from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class NotificationState:
    user_id: int
    timeshift: time
    id_: int | None = None
    times: list["NotificationTime"] = field(default_factory=list)


@dataclass
class NotificationTime:
    time: time
    id_: int | None = None
