from aiogram import types, Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode, ShowMode

from ..FSM import CommonFSM

common_commands_router = Router(name="common_commands")


@common_commands_router.message(Command("start", "cancel"))
async def command_start_process(message: types.Message,
                                dialog_manager: DialogManager):
    preparing_message = await message.answer(
        text="Подготовка...",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await preparing_message.delete()
    await dialog_manager.start(
        state=CommonFSM.state,
        mode=StartMode.RESET_STACK
    )


@common_commands_router.message(Command("menu"))
async def command_menu(message: types.Message,
                       dialog_manager: DialogManager):
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.delete()
    await dialog_manager.update({})
