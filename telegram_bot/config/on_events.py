import logging

from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from common.ORM.database import Session
from common.middlewares import DbSessionMiddleware, ContextMiddleware, register_middlewares
from config import settings
from config.logger import init_logging
from config.scheduler import NotificationScheduler
from config.ui_config import set_ui_commands
from http_server.webhook import init_webhook


async def on_startup(dispatcher: Dispatcher,
                     bot: Bot,
                     **__):
    init_logging()

    scheduler = NotificationScheduler(timezone=settings.TIMEZONE)
    scheduler.start()
    await scheduler.init(bot)

    middlewares = [
        ContextMiddleware(scheduler=scheduler),
        DbSessionMiddleware(session_pool=Session),
        CallbackAnswerMiddleware()
    ]
    register_middlewares(middlewares, dispatcher)

    await set_ui_commands(bot)

    await bot.delete_webhook()
    await init_webhook(bot)


async def on_shutdown(dispatcher: Dispatcher,
                      bot: Bot):
    logging.info("SHUTDOWN")
    await bot.delete_webhook()
    await bot.session.close()
