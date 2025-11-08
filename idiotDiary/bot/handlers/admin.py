from aiogram import F
from aiogram import Router, types

from idiotDiary.bot.filters.base import set_filter_on_router
from idiotDiary.bot.filters.user import role_filter


async def get_message_info(message: types.Message):
    forward_origin = message.forward_origin
    text = ""
    if forward_origin.type != "hidden_user":
        text += f"User ID: {forward_origin.sender_user.id}\n"
    text += f"Chat ID: {message.chat.id}\nFrom User ID: {message.from_user.id}\n"
    await message.answer(text)


def setup():
    router = Router(name=__name__)
    set_filter_on_router(router, role_filter(allow_superuser=True))

    router.message.register(get_message_info, F.forward_origin.is_not(None))

    return router
