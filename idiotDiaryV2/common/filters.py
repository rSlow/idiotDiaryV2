import re
from re import Pattern
from typing import Any

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from common.types import UserIDType
from config import settings


class UserIDFilter(BaseFilter):
    def __init__(self, users_id: UserIDType):

        if not isinstance(users_id, list | tuple):
            users_id = (users_id,)
        self.users_id = users_id

    async def __call__(self,
                       obj: TelegramObject,
                       raw_state: str | None = None) -> bool | dict[str, Any]:
        if str(obj.from_user.id) not in self.users_id:
            return False
        return True


class OwnerFilter(UserIDFilter):
    def __init__(self):
        super().__init__(settings.OWNER_ID)


def regexp_factory(pattern: str | Pattern[str]):
    def _factory(value: str):
        res = re.match(pattern, value)
        if res is None:
            raise ValueError
        return value

    return _factory
