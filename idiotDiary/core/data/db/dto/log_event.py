from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogEvent:
    type_: str
    chat_id: int
    dt: datetime
    user_id: int | None = None
    content_type: str | None = None
    data: str | None = None
