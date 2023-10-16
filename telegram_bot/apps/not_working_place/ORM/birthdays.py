from datetime import date, timedelta, datetime

from sqlalchemy import select, extract, and_, delete
from sqlalchemy.orm import Mapped, mapped_column

from ..http_app.schemas import SBirthday
from common.ORM.database import Base, Session
from config import settings


class Birthday(Base):
    __tablename__ = "birthdays"

    id: Mapped[int] = mapped_column(primary_key=True)
    fio: Mapped[str] = mapped_column(primary_key=True)
    date: Mapped[date]
    post: Mapped[str]
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
