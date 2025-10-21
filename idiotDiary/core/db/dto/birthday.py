from dataclasses import dataclass
from datetime import date as d
from uuid import UUID

from idiotDiary.core.utils.dates import get_now


@dataclass
class Birthday:
    uuid: UUID
    fio: str
    date: d
    post: str | None = None
    rank: str | None = None

    @property
    def age(self):
        return int(round((get_now().date() - self.date).days / 362.25))
