import logging

from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats

from idiotDiary.bot.views import commands as c

logger = logging.getLogger(__name__)


async def setup(bot: Bot):
    commands = [
        c.START,
        c.HELP,
        c.ABOUT,
        c.UPDATE,
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats()
    )
    logger.info("%s bot commands were installed.", len(commands))
