import logging

from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from common.middlewares import DbSessionMiddleware, ContextMiddleware
from common.storage import memory_storage
from common.ORM.database import Session
from config.logger import init_logging
from config.scheduler import scheduler, init_schedules
from config.ui_config import set_ui_commands
from http_server.webhook import init_webhook


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    init_logging()

    dispatcher.update.middleware(ContextMiddleware(
        scheduler=scheduler,
    ))
    dispatcher.update.middleware(DbSessionMiddleware(session_pool=Session))
    dispatcher.update.middleware(CallbackAnswerMiddleware())

    await memory_storage.set_all_states(also_to_db=False)
    await set_ui_commands(bot)

    scheduler.start()
    init_schedules(bot)

    await bot.delete_webhook()
    await init_webhook(dispatcher, bot)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.info("SHUTDOWN")
    await bot.delete_webhook()
    await bot.session.close()
