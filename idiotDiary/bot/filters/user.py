from typing import cast

from aiogram import types
from magic_filter import MagicFilter

from idiotDiary.bot.filters.base import F_MD
from idiotDiary.core.db import dto

F_User = cast(MagicFilter, F_MD["user"])
F_User_roles = cast(MagicFilter, F_User.roles)


def is_superuser(superusers: list[int]):
    async def _is_superuser(message: types.Message) -> bool:
        user = message.from_user
        if not isinstance(user, types.User):
            raise TypeError(
                f"user {str(user)} is {type(user)}, not <types.User> type"
            )
        return user.id in superusers

    return _is_superuser


def role_filter(role_name: str):
    async def _role_filter(_, user: dto.User, **__) -> bool:
        return role_name in user.roles

    return _role_filter
