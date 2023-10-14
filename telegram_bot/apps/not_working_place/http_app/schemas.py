from datetime import date

import pydantic


class SBirthday(pydantic.BaseModel):
    fio: str
    date: date
    post: str
    rank: str | None = None

    class Config:
        from_attributes = True
