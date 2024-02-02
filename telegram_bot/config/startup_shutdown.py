import logging

from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from common.ORM.database import Session
from common.context_message import ContextMessageManager
from common.middlewares import DbSessionMiddleware, ContextMiddleware
from config import settings
from config.logger import init_logging
from config.scheduler import NotificationScheduler
from config.ui_config import set_ui_commands
from http_server.webhook import init_webhook


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    init_logging()

    scheduler = NotificationScheduler(timezone=settings.TIMEZONE)
    scheduler.start()
    await scheduler.init(bot)

    dispatcher.update.middleware(ContextMiddleware(
        scheduler=scheduler,
        message_manager=ContextMessageManager
    ))
    dispatcher.update.middleware(DbSessionMiddleware(session_pool=Session))
    dispatcher.update.middleware(CallbackAnswerMiddleware())

    await set_ui_commands(bot)

    await bot.delete_webhook()
    await init_webhook(bot)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.info("SHUTDOWN")
    await bot.delete_webhook()
    await bot.session.close()
