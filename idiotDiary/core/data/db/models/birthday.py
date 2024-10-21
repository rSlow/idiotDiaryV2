from datetime import date
from uuid import UUID

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from idiotDiary.core.data.db import dto
from .base import Base


class Birthday(Base):
    __tablename__ = "birthdays"

    uuid: Mapped[UUID] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    fio: Mapped[str]
    date: Mapped[date]
    post: Mapped[str | None]
    rank: Mapped[str | None]

    @property
    def as_dto(self):
        return dto.Birthday(
            user_id=self.user_id,
            fio=self.fio,
            date=self.date,
            uuid=self.uuid,
            post=self.post,
            rank=self.rank
        )
