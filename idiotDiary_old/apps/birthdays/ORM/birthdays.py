from datetime import date
from typing import Sequence, Self
from uuid import UUID

from sqlalchemy import select, and_, delete, BigInteger, extract
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from common.ORM.database import Base
from common.utils.functions import get_now
from ..http_app.schemas import SBirthday


class Birthday(Base):
    __tablename__ = "birthdays"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    fio: Mapped[str]
    date: Mapped[date]
    post: Mapped[str] = mapped_column(nullable=True)
    rank: Mapped[str] = mapped_column(nullable=True)

    @property
    def age(self):
        return int(round((get_now().date() - self.date).days / 362.25))

    def get_declension(self):
        age = self.age
        if age % 10 == 1 and age != 11:
            return "год"
        elif age % 10 in [2, 3, 4] and (age < 10 or age > 20):
            return "года"
        return "лет"

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
    async def get_birthdays_in_date(cls,
                                    user_id: int,
                                    session: AsyncSession,
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
    async def delete_birthday(cls,
                              user_id: int,
                              uuid: UUID,
                              session: AsyncSession) -> bool:
        q = select(cls).filter(
            cls.uuid == uuid,
            cls.user_id == user_id
        )
        res = await session.execute(q)
        birthday: Self | None = res.scalars().one_or_none()
        await session.close()

        if birthday is None:
            return False
        else:
            async with session.begin():
                q = delete(cls).filter(
                    cls.uuid == birthday.uuid,
                    cls.user_id == user_id
                )
                await session.execute(q)
            return True
