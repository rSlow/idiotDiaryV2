from datetime import date

from pydantic import UUID4, BaseModel


class SBirthday(BaseModel):
    uuid: UUID4
    fio: str
    date: date
    post: str | None = None
    rank: str | None = None

    class Config:
        from_attributes = True
