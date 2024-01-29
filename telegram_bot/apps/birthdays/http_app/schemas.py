from datetime import date, time
from typing import Annotated
from uuid import UUID

from pydantic import UUID4, AfterValidator, BaseModel


class UUIDValidationError(TypeError):
    pass


def uuid_validator(v: str):
    try:
        return UUID(v, version=4)
    except ValueError:
        raise UUIDValidationError()


class SBirthday(BaseModel):
    uuid: UUID4 | Annotated[str, AfterValidator(uuid_validator)]
    fio: str
    date: date
    post: str | None = None
    rank: str | None = None

    class Config:
        from_attributes = True
