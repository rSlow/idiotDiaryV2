from datetime import date
from typing import Annotated
from uuid import UUID

import pydantic
from pydantic import Field, UUID4, AfterValidator


def uuid_validator(v: str):
    return UUID(v, version=4)


class SBirthday(pydantic.BaseModel):
    uuid: UUID4 | Annotated[str, AfterValidator(uuid_validator)]
    fio: str
    date: date
    post: str | None = None
    rank: str | None = None

    class Config:
        from_attributes = True
