from datetime import date, timedelta, datetime
from uuid import UUID

from sqlalchemy import select, extract, and_, delete
from sqlalchemy.orm import Mapped, mapped_column

from ..http_app.schemas import SBirthday
from common.ORM.database import Base, Session
from config import settings


class Birthday(Base):
    __tablename__ = "birthdays"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    fio: Mapped[str] = mapped_column()
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
    async def delete_data(cls):
        async with Session() as session:
            async with session.begin():
                q = delete(cls)
                await session.execute(q)

    @classmethod
    async def get_date_list(cls, d: date):
        async with Session() as session:
            q = select(cls).filter(
                and_(
                    extract('month', cls.date) == d.month,
                    extract('day', cls.date) == d.day
                ))
            result = await session.execute(q)
            date_list: list[cls] = result.scalars().all()
        return date_list

    @classmethod
    async def get_today_list(cls):
        today = datetime.now().astimezone(settings.TIMEZONE).date()
        return await cls.get_date_list(today)

    @classmethod
    async def get_tomorrow_list(cls):
        today = datetime.now().astimezone(settings.TIMEZONE).date()
        tomorrow = today + timedelta(days=1)
        return await cls.get_date_list(tomorrow)

    @classmethod
    async def delete_birthday(cls, uuid: UUID):
        async with Session() as session:
            q = select(cls).filter_by(
                uuid=uuid
            )
            res = await session.execute(q)
            birthday: cls | None = res.scalars().one_or_none()

            if birthday is None:
                return False
            else:
                await session.delete(birthday)
                return True
