import logging

from aiogram import Bot, Dispatcher

from common.middlewares import DbSessionMiddleware
from common.storage import memory_storage
from common.ORM.database import Session
from config.logger import init_logging
from config.ui_config import set_ui_commands
from http_server.webhook import init_webhook


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    init_logging()

    dispatcher.update.middleware(DbSessionMiddleware(session_pool=Session))

    await memory_storage.set_all_states()
    await set_ui_commands(bot)

    await init_webhook(dispatcher, bot)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.info("SHUTDOWN")
    await bot.delete_webhook()
