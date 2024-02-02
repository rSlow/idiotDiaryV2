from datetime import time
from typing import Self, Sequence, Optional

from sqlalchemy import select, delete, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from common.ORM.database import Base, Session


class NotificationUser(Base):
    __tablename__ = "notification_users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    timeshift: Mapped[time] = mapped_column(nullable=True, default=lambda: time(hour=0, minute=0))
    times: Mapped[list["NotificationTime"]] = relationship()

    @classmethod
    async def get_all(cls) -> Sequence[Self]:
        async with Session() as session:
            q = select(cls).options(selectinload(cls.times))
            res = await session.execute(q)
            return res.scalars().all()

    @classmethod
    async def get_user(cls,
                       session: AsyncSession,
                       user_id: int) -> Self:
        q = select(
            cls
        ).filter(
            cls.user_id == user_id
        )
        res = await session.execute(q)
        return res.scalars().one_or_none()

    @classmethod
    async def add_or_update_user(cls,
                                 session: AsyncSession,
                                 user_id: int,
                                 timeshift: Optional[time] = None) -> None:
        async with session.begin():
            q = select(cls).filter(
                cls.user_id == user_id
            )
            res = await session.execute(q)
            user = res.scalars().one_or_none()
            if user:
                user.timeshift = timeshift
            else:
                session.add(cls(
                    user_id=user_id,
                    timeshift=timeshift
                ))


class NotificationTime(Base):
    __tablename__ = "notification_times"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("notification_users.user_id"))
    time: Mapped[time]

    @classmethod
    async def delete_notification(cls,
                                  session: AsyncSession,
                                  user_id: int,
                                  notification_time: time) -> None:
        async with session.begin():
            get_q = select(cls).filter(
                cls.user_id == user_id,
                cls.time == notification_time
            )
            get_res = await session.execute(get_q)
            time_to_del = get_res.scalars().one()
            await session.delete(time_to_del)

    @classmethod
    async def add_notification(cls,
                               session: AsyncSession,
                               user_id: int,
                               notification_time: time) -> None:
        user = await NotificationUser.get_user(
            session=session,
            user_id=user_id
        )
        await session.close()
        if user is None:
            await NotificationUser.add_or_update_user(
                session=session,
                user_id=user_id
            )
        async with session.begin():
            session.add(cls(
                user_id=user_id,
                time=notification_time,
            ))

    @classmethod
    async def get_notifications(cls,
                                session: AsyncSession,
                                user_id: int) -> Sequence[Self]:
        q = select(cls).filter(
            cls.user_id == user_id
        )
        res = await session.execute(q)
        return res.scalars().all()

    @classmethod
    async def clear_notifications(cls,
                                  session: AsyncSession,
                                  user_id: int) -> None:
        async with session.begin():
            q = delete(cls).filter(
                cls.user_id == user_id
            )
            await session.execute(q)
