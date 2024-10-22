from aiogram import types, Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog import StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from idiotDiary.bot.di.jinja import JinjaRenderer
from idiotDiary.bot.states.start import MainMenuSG
from idiotDiary.bot.views import commands


async def cmd_start(message: types.Message, dialog_manager: DialogManager):
    await message.answer("тут будет стартовый текст")
    await dialog_manager.start(
        state=MainMenuSG.state, mode=StartMode.RESET_STACK
    )


@inject
async def cmd_help(
        message: types.Message, dialog_manager: DialogManager,
        jinja: FromDishka[JinjaRenderer]
):
    help_message = jinja.render_template("help.jinja2")
    await message.answer(help_message)
    await dialog_manager.update({}, show_mode=ShowMode.DELETE_AND_SEND)


async def cmd_about(message: types.Message, dialog_manager: DialogManager):
    await message.answer(f"Разработчик бота - @rs1ow.\n")
    await dialog_manager.update({}, show_mode=ShowMode.DELETE_AND_SEND)


async def cmd_update(message: types.Message, dialog_manager: DialogManager):
    await message.delete()
    await dialog_manager.update({}, show_mode=ShowMode.DELETE_AND_SEND)


def setup():
    router = Router(name=__name__)

    router.message.register(cmd_start, Command(commands.START))
    router.message.register(cmd_help, Command(commands.HELP))
    router.message.register(cmd_about, Command(commands.ABOUT))
    router.message.register(cmd_update, Command(commands.UPDATE))

    return router
