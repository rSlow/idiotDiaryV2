import logging

from aiogram import Dispatcher, Router

from idiotDiary.bot.filters.private import set_chat_private_filter, set_chat_group_filter
from . import commands, birthdays, not_working_place, admin
from . import errors

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, log_chat_id: int):
    private_handlers_router = Router(name=__name__)
    set_chat_private_filter(private_handlers_router)

    chat_router = Router(name=__name__ + "_chat")
    set_chat_group_filter(chat_router)

    errors.setup(dp, log_chat_id)

    private_handlers_router.include_routers(commands.setup())
    private_handlers_router.include_routers(admin.setup())
    # private_handlers_router.include_routers(birthdays.setup())

    chat_router.include_routers(not_working_place.setup_chat())

    dp.include_router(private_handlers_router)
    dp.include_router(chat_router)

    logger.debug("handlers configured successfully")
