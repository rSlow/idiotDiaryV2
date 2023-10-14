from typing import Any

from aiogram import Bot, Dispatcher, types
from fastapi import FastAPI, Header, HTTPException, status, APIRouter

from config import settings

webhook_router = APIRouter()


async def init_webhook(dp: Dispatcher, bot: Bot):
    await bot.set_webhook(
        url=f"{settings.BASE_WEBHOOK_URL}{settings.WEBHOOK_PATH}",
        secret_token=settings.WEBHOOK_SECRET
    )

    @webhook_router.post(settings.WEBHOOK_PATH)
    async def bot_webhook(update: dict,
                          secret_token: str = Header(alias=settings.SECRET_HEADER)):
        if secret_token != settings.WEBHOOK_SECRET:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect secret token",
            )

        telegram_update = types.Update(**update)
        await dp.feed_update(bot=bot, update=telegram_update)


def fastapi_setup(fastapi_app: FastAPI, dispatcher: Dispatcher, /, **kwargs: Any) -> None:
    workflow_data = {
        "app": fastapi_app,
        "dispatcher": dispatcher,
        **dispatcher.workflow_data,
        **kwargs,
    }

    async def on_startup(*_: Any, **__: Any):
        await dispatcher.emit_startup(**workflow_data)

    async def on_shutdown(*_: Any, **__: Any):
        await dispatcher.emit_shutdown(**workflow_data)

    fastapi_app.add_event_handler("startup", on_startup)
    fastapi_app.add_event_handler("shutdown", on_shutdown)
