from typing import Callable

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable

from idiotDiary.bot.middlewares.config import MiddlewareData


def is_superuser(superusers: list[int]) -> Callable:
    async def _is_superuser(message: types.Message) -> bool:
        user = message.from_user
        if not isinstance(user, types.User):
            raise TypeError(
                f"user {str(user)} is {type(user)}, not 'types.User' type"
            )
        return user.id in superusers

    return _is_superuser


def adg_is_superuser(data: dict, _: Whenable, __: DialogManager):
    middleware_data: MiddlewareData = data["middleware_data"]
    user = middleware_data["user"]
    superusers = middleware_data["bot_config"].superusers
    return user.tg_id in superusers
