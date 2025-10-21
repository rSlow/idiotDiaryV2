from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog.api.entities import DialogUpdateEvent

from idiotDiary.bot.middlewares.config import MiddlewareData
from idiotDiary.core.db import dto
from idiotDiary.core.db.dao import UserDao


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData,
    ) -> Any:
        dishka = data["dishka_container"]
        user_tg = data.get("event_from_user", None)
        if user_tg is None:
            user = None
        else:
            user_dao = await dishka.get(UserDao)
            if isinstance(event, DialogUpdateEvent):
                user = await user_dao.get_by_tg_id(user_tg.id)
            else:
                user = await user_dao.upsert_user(dto.User.from_aiogram(user_tg))
        data["user"] = user

        return await handler(event, data)
