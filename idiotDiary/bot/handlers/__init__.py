import logging

from aiogram import Dispatcher

from idiotDiary.bot.config.models.bot import BotConfig
from . import commands
from . import errors

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher):
    errors.setup(dp)

    dp.include_routers(commands.setup())

    logger.debug("handlers configured successfully")
