from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import User
from aiogram_dialog import DialogManager, StartMode, Dialog, Window, LaunchMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Column, Start

from apps.admin.FSM.admin import AdminFSM
from apps.birthdays.states import BirthdaysFSM
from apps.free_shaurma.FSM import FShStartFSM
from apps.music.states import MusicMainFSM
from ..FSM import CommonFSM
from apps.not_working_place.states import NWPStartFSM
from ..whens import WhenOwner, WhenBirthdays

start_router = Router(name="start")


async def username_getter(event_from_user: User, **__):
    return {'username': event_from_user.username or event_from_user.full_name}


@start_router.message(Command("start", "cancel"))
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


main_menu = Dialog(
    Window(
        Format("{username}, куда надо?"),
        Column(
            Start(
                Const("нерабочая площадка 😶‍🌫️"),
                id="not_working_place",
                state=NWPStartFSM.state
            ),
            Start(
                Const("(бес)платная шаурма 🌯"),
                id="free_shaurma",
                state=FShStartFSM.device
            ),
            Start(
                Const("напоминальщик ДР 🎂"),
                id="birthdays",
                state=BirthdaysFSM.state,
                when=WhenBirthdays()
            ),
            Start(
                Const("Музыка 🎧"),
                id="music",
                state=MusicMainFSM.state
            ),
            Start(
                Const("Админка ⚙️"),
                id="admin",
                state=AdminFSM.state,
                when=WhenOwner()
            ),
        ),
        getter=username_getter,
        state=CommonFSM.state,
    ),
    launch_mode=LaunchMode.ROOT
)
