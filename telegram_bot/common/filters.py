from abc import ABC
from typing import Any, Iterable

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject, Message

from config import settings
from .keyboards.base import YesNoKeyboard, BackKeyboard

UserIDType = str | Iterable[str]


class MessageTextFilter(BaseFilter, ABC):
    def __init__(self, text: str):
        self.text = text

    async def __call__(self, message: Message):
        if message.text == self.text:
            return True
        return False


class YesKeyboardFilter(MessageTextFilter):
    def __init__(self):
        super().__init__(text=YesNoKeyboard.Buttons.yes)


class NoKeyboardFilter(MessageTextFilter):
    def __init__(self):
        super().__init__(text=YesNoKeyboard.Buttons.no)


class BackFilter(MessageTextFilter):
    def __init__(self):
        super().__init__(text=BackKeyboard.Buttons.back)


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


class BirthdaysAllowedFilter(UserIDFilter):
    def __init__(self):
        super().__init__(settings.BIRTHDAYS_ALLOWED)
