from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from idiotDiary.core.data.db import models as db, dto
from idiotDiary.core.data.db.dao.base import BaseDao


class BirthdayDao(BaseDao[db.Birthday]):
    def __init__(self, session: AsyncSession):
        super().__init__(db.Birthday, session)

    async def update(self, birthdays: list[dto.Birthday], user: dto.User):
        await self.session.execute(
            delete(self.model)
            .filter(
                self.model.uuid.in_([birthday.uuid for birthday in birthdays]),
                self.model.user_id == user.tg_id
            )
        )
        models = [
            self.model(
                fio=birthday.fio, date=birthday.date, uuid=birthday.uuid,
                post=birthday.post, rank=birthday.rank, user_id=user.tg_id
            )
            for birthday in birthdays
        ]
        self.session.add_all(models)
        await self.session.commit()

    async def delete_all_from_user(self, user: dto.User):
        await self.session.execute(
            delete(self.model)
            .filter(self.model.user_id == user.tg_id)
        )
        await self.session.commit()

    async def delete(self, birthday_uuid: UUID):
        res = await self.session.execute(
            select(self.model)
            .filter(self.model.uuid == birthday_uuid)
        )
        birthday: db.Birthday | None = res.one_or_none()

        if birthday is None:
            raise BirthdayNotExist()

        await self.session.execute(
            delete(self.model)
            .filter(self.model.uuid == birthday.uuid)
        )
        await self.session.commit()
