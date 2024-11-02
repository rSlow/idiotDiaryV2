from sqlalchemy import ScalarResult, select, Result, update, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import selectinload

from idiotDiary.core.db import dto
from idiotDiary.core.db import models as db
from idiotDiary.core.db.dao.base import BaseDao
from idiotDiary.core.utils.exceptions.user import NoUsernameFound, \
    MultipleUsernameFound


class UserDao(BaseDao[db.User]):
    async def get_by_tg_id(self, tg_id: int) -> dto.User:
        result: ScalarResult[db.User] = await self.session.scalars(
            select(self.model)
            .where(self.model.tg_id == tg_id)
            .options(*user_options())
        )
        user = result.one()
        return user.to_dto()

    async def get_by_id(self, id_: int) -> dto.User:
        result = await self.session.scalars(
            select(self.model)
            .where(self.model.id == id_)
            .options(*user_options())
        )
        return result.one().to_dto()

    async def _get_by_username(self, username: str) -> db.User:
        result: Result[tuple[db.User]] = await self.session.execute(
            select(self.model)
            .where(self.model.username == username)
            .options(*user_options())
        )

        try:
            user = result.scalar_one()
        except MultipleResultsFound as e:
            raise MultipleUsernameFound(username=username) from e
        except NoResultFound as e:
            raise NoUsernameFound(username=username) from e

        return user

    async def upsert_user(self, user: dto.User) -> dto.User:
        kwargs = {
            "tg_id": user.tg_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "is_bot": user.is_bot,
        }
        await self.session.execute(
            insert(self.model)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(self.model.tg_id,),
                set_=kwargs,
                where=self.model.tg_id == user.tg_id
            )
        )
        await self.commit()
        saved_user = await self.get_by_tg_id(user.tg_id)
        return saved_user

    async def get_by_username(self, username: str):
        user = await self._get_by_username(username)
        return user.to_dto()

    async def get_by_username_with_password(self, username: str):
        user = await self._get_by_username(username)
        return user.to_dto().with_password(user.hashed_password)

    async def set_password(self, user: dto.User, hashed_password: str):
        db_user = await self._get_by_id(user.id_)
        db_user.hashed_password = hashed_password
        await self.commit()

    async def get_all_active(self):
        result = await self.session.execute(
            select(self.model.tg_id)
            .where(self.model.is_active.is_(True))
        )
        user_ids = result.scalars().all()
        return user_ids

    async def deactivate(self, tg_id: int):
        await self.session.execute(
            update(self.model)
            .where(self.model.tg_id == tg_id)
            .values(is_active=False)
        )
        await self.commit()

    async def get_all_with_role(self, role_id: int):
        res = await self.session.scalars(
            select(self.model)
            .join(db.UsersRoles)
            .join(db.Role)
            .where(db.Role.id == role_id)
            .options(*user_options())
        )
        return [user.to_dto() for user in res.all()]

    async def count_with_role(self, role_id: int):
        res = await self.session.scalars(
            select(func.count(self.model.id))
            .join(db.UsersRoles)
            .join(db.Role)
            .where(db.Role.id == role_id)
        )
        return res.one()


def user_options():
    return (
        selectinload(db.User.roles),
    )
