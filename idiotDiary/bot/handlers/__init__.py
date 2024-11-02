import logging

from aiogram import Dispatcher

from . import commands, birthdays
from . import errors

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher):
    errors.setup(dp)

    dp.include_routers(commands.setup())
    dp.include_routers(birthdays.setup())

    logger.debug("handlers configured successfully")
