from aiogram import Router, types
from aiogram.filters import Command
from aiogram_dialog import DialogManager, ShowMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from idiotDiary.bot.di.jinja import JinjaRenderer
from idiotDiary.bot.filters.user import role_filter
from idiotDiary.bot.views import commands
from idiotDiary.bot.views.birthdays import get_birthdays_message
from idiotDiary.core.db import dto
from idiotDiary.core.db.dao.birthday import BirthdayDao

birthdays_router = Router(name="birthdays")


@inject
async def check_birthdays(
        message: types.Message, dialog_manager: DialogManager,
        dao: FromDishka[BirthdayDao], jinja: FromDishka[JinjaRenderer]
):
    user: dto.User = dialog_manager.middleware_data["user"]
    if "birthdays" in user.roles:
        message_text = await get_birthdays_message(dao, user.id_, jinja)
        await message.answer(message_text, disable_notification=True)
    await dialog_manager.update({}, ShowMode.DELETE_AND_SEND)


def setup():
    router = Router(name=__name__)
    router.message.filter(role_filter("birthdays"))

    router.message.register(check_birthdays, Command(commands.BIRTHDAYS))

    return router
