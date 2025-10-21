from aiogram import Router

from idiotDiary.bot.filters.user import role_filter
from idiotDiary.bot.handlers.birthdays import messages

birthdays_router = Router(name="birthdays")


def setup():
    router = Router(name=__name__)
    router.message.filter(role_filter("birthdays"))

    router.include_router(messages.setup())

    return router
