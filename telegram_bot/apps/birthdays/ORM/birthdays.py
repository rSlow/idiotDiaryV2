from datetime import date
from typing import Sequence, Self
from uuid import UUID

from sqlalchemy import select, extract, and_, delete, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from ..http_app.schemas import SBirthday
from common.ORM.database import Base, Session


class Birthday(Base):
    __tablename__ = "birthdays"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    fio: Mapped[str]
    date: Mapped[date]
    post: Mapped[str] = mapped_column(nullable=True)
    rank: Mapped[str] = mapped_column(nullable=True)

    @classmethod
    async def update_data(cls, data: list[SBirthday]):
        async with Session() as session:
            async with session.begin():
                q = delete(cls).filter(
                    cls.fio.in_([birthday.fio for birthday in data])
                )
                await session.execute(q)

                session.add_all([
                    cls(**birthday.model_dump())
                    for birthday in data
                ])

    @classmethod
    async def delete_data(cls,
                          user_id: int):
        async with Session() as session:
            async with session.begin():
                q = delete(cls).filter(
                    cls.user_id == user_id
                )
                await session.execute(q)

    @classmethod
    async def get_birthdays_in_date(cls,
                                    session: AsyncSession,
                                    user_id: int,
                                    d: date) -> Sequence[Self]:
        q = select(cls).filter(
            and_(
                extract('month', cls.date) == d.month,
                extract('day', cls.date) == d.day,
                cls.user_id == user_id
            ),
        )
        result = await session.execute(q)
        birthdays = result.scalars().all()
        return birthdays

    @classmethod
    async def delete_birthday(cls, uuid: UUID) -> bool:
        async with Session() as session:
            q = select(cls).filter_by(
                uuid=uuid
            )
            res = await session.execute(q)
            birthday: cls | None = res.scalars().one_or_none()

            if birthday is None:
                return False
            else:
                q = delete(cls).filter(cls.uuid == birthday.uuid)
                await session.execute(q)
                return True
