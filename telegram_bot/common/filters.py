from typing import Any, Iterable

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject, Message

from .keyboards.base import YesNoKeyboard, BackKeyboard
from config import settings

UserIDType = int | str | Iterable[int] | Iterable[str]


class YesKeyboardFilter(BaseFilter):
    async def __call__(self, message: Message):
        if message.text == YesNoKeyboard.Buttons.yes:
            return True
        return False


class BackFilter(BaseFilter):
    async def __call__(self, message: Message):
        if message.text == BackKeyboard.Buttons.back:
            return True
        return False


class NoKeyboardFilter(BaseFilter):
    async def __call__(self, message: Message):
        if message.text == YesNoKeyboard.Buttons.no:
            return True
        return False


class UserIDFilter(BaseFilter):
    def __init__(self, users_id: UserIDType):

        if not isinstance(users_id, Iterable):
            users_id = [users_id]
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


class BirthdaysAllowedFilter(UserIDFilter):
    def __init__(self):
        super().__init__(settings.BIRTHDAYS_ALLOWED)
