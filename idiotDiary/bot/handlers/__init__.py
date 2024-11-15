import logging

from aiogram import Dispatcher

from . import commands, birthdays
from . import errors

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, log_chat_id: int):
    errors.setup(dp, log_chat_id)

    dp.include_routers(commands.setup())
    dp.include_routers(birthdays.setup())

    logger.debug("handlers configured successfully")
