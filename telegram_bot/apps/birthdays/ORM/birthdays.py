from datetime import date
from typing import Sequence, Self, Optional
from uuid import UUID

from sqlalchemy import select, extract, and_, delete, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from common.ORM.database import Base
from ..http_app.schemas import SBirthday


class Birthday(Base):
    __tablename__ = "birthdays"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    fio: Mapped[str]
    date: Mapped[date]
    post: Mapped[str] = mapped_column(nullable=True)
    rank: Mapped[str] = mapped_column(nullable=True)

    @classmethod
    async def update_data(cls,
                          user_id: int,
                          data: list[SBirthday],
                          session: AsyncSession) -> None:
        async with session.begin():
            q = delete(cls).filter(
                cls.uuid.in_([birthday.uuid for birthday in data]),
                cls.user_id == user_id
            )
            await session.execute(q)

            session.add_all([
                cls(**birthday.model_dump(),
                    user_id=user_id)
                for birthday in data
            ])

    @classmethod
    async def delete_data(cls,
                          user_id: int,
                          session: AsyncSession) -> None:
        async with session.begin():
            q = delete(cls).filter(
                cls.user_id == user_id
            )
            await session.execute(q)

    @classmethod
    async def get_birthdays_in_dates(cls,
                                     user_id: int,
                                     session: AsyncSession,
                                     start_date: date,
                                     end_date: Optional[date] = None) -> Sequence[Self]:
        if end_date is None:
            end_date = start_date
        q = select(cls).filter(
            and_(
                extract('month', cls.date) >= start_date.month,
                extract('day', cls.date) >= start_date.day,
                extract('month', cls.date) <= end_date.month,
                extract('day', cls.date) <= end_date.day,
                cls.user_id == user_id
            ),
        )
        result = await session.execute(q)
        birthdays = result.scalars().all()
        return birthdays

    @classmethod
    async def delete_birthday(cls,
                              user_id: int,
                              uuid: UUID,
                              session: AsyncSession) -> bool:
        q = select(cls).filter(
            cls.uuid == uuid,
            cls.user_id == user_id
        )
        res = await session.execute(q)
        birthday: cls | None = res.scalars().one_or_none()

        if birthday is None:
            return False
        else:
            q = delete(cls).filter(
                cls.uuid == birthday.uuid
            )
            await session.execute(q)
            return True
