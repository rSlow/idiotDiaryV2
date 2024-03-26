from typing import Any

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import async_sessionmaker

from common.types import HandlerType


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: HandlerType,
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)


class ContextMiddleware(BaseMiddleware):
    def __init__(self, **context):
        super().__init__()
        self.context = context

    async def __call__(
            self,
            handler: HandlerType,
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        data.update(self.context)

        event_from_user: User = data.get("event_from_user")
        data["user_id"] = event_from_user.id

        return await handler(event, data)


def register_middlewares(middlewares: list[BaseMiddleware],
                         dispatcher: Dispatcher):
    for middleware in middlewares:
        dispatcher.update.middleware(middleware)
        dispatcher.error.middleware(middleware)
