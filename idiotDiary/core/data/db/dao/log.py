from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from idiotDiary.core.data.db import models as db, dto
from idiotDiary.core.data.db.dao.base import BaseDao


class EventLogDao(BaseDao[db.LogEvent]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(db.LogEvent, session)

    async def get_last_from_user(self, user_id: int) -> dto.LogEvent | None:
        res = await self.session.scalars(
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(desc(self.model.dt))
            .limit(1)
        )
        event = res.all()
        return event[0].to_dto() if event else None

    async def write_event(self, event: dto.LogEvent) -> None:
        self.session.add(
            db.LogEvent(
                event_type=event.type_,
                chat_id=event.chat_id,
                dt=event.dt,
                user_id=event.user_id,
                content_type=event.content_type,
                data=event.data
            )
        )
        await self.commit()
