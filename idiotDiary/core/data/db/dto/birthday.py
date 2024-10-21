from dataclasses import dataclass
from datetime import date as d
from uuid import UUID


@dataclass
class Birthday:
    user_id: int
    fio: str
    date: d
    uuid: UUID | None = None
    post: str | None = None
    rank: str | None = None

    @property
    def age(self):
        return int(round((get_now().date() - self.date).days / 362.25))
