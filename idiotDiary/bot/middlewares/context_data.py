from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog.api.entities import DialogUpdateEvent

from idiotDiary.bot.config.models import BotConfig
from idiotDiary.bot.middlewares.config import MiddlewareData
from idiotDiary.bot.views.alert import BotAlert
from idiotDiary.core.data.db import dto
from idiotDiary.core.data.db.dao import DaoHolder
from idiotDiary.core.scheduler.scheduler import Scheduler
from idiotDiary.core.utils.lock_factory import LockFactory


class ContextDataMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData,
    ) -> Any:
        dishka = data["dishka_container"]
        dao_holder: DaoHolder = await dishka.get(DaoHolder)
        data["bot_config"] = await dishka.get(BotConfig)
        data["locker"] = await dishka.get(LockFactory)
        data["scheduler"] = await dishka.get(Scheduler)
        data["alert"] = await dishka.get(BotAlert)
        data["dao"] = dao_holder

        user_tg = data.get("event_from_user", None)
        if user_tg is None:
            user = None
        else:
            if isinstance(event, DialogUpdateEvent):
                user = await dao_holder.user.get_by_tg_id(user_tg.id)
            else:
                user = await dao_holder.user.upsert_user(
                    dto.User.from_aiogram(user_tg)
                )
        data["user"] = user

        return await handler(event, data)
