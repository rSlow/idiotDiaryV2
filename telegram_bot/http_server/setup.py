from typing import Any

from aiogram import Dispatcher, Bot
from fastapi import FastAPI

from config.bot import init_dispatcher


def fastapi_setup(fastapi_app: FastAPI,
                  dispatcher: Dispatcher,
                  bot: Bot,
                  **kwargs: Any) -> None:
    workflow_data = {
        "app": fastapi_app,
        "dispatcher": dispatcher,
        "bot": bot,
        **dispatcher.workflow_data,
        **kwargs,
    }

    async def on_startup(*_: Any, **__: Any):
        init_dispatcher(dispatcher)
        await dispatcher.emit_startup(**workflow_data)

    async def on_shutdown(*_: Any, **__: Any):
        await dispatcher.emit_shutdown(**workflow_data)

    fastapi_app.add_event_handler("startup", on_startup)
    fastapi_app.add_event_handler("shutdown", on_shutdown)
