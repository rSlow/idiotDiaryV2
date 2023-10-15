import logging
from typing import Any

from aiogram import Bot, Dispatcher
from fastapi import FastAPI

from config import settings


async def init_webhook(dp: Dispatcher, bot: Bot):
    webhook_url = f"{settings.BASE_WEBHOOK_URL}{settings.WEBHOOK_PATH}"
    await bot.set_webhook(
        url=webhook_url,
        secret_token=settings.WEBHOOK_SECRET
    )
    logging.info("SET WEBHOOK")


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
