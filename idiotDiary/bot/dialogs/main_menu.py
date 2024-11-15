from aiogram.types import User
from aiogram_dialog import Dialog, Window, LaunchMode
from aiogram_dialog.widgets.kbd import Column, Start
from aiogram_dialog.widgets.text import Format, Const
from dishka.integrations.aiogram_dialog import inject

from idiotDiary.bot.filters.user import F_User
from idiotDiary.bot.states.admin import AdminMainSG
from idiotDiary.bot.states.birthdays import BirthdaysMenuSG
from idiotDiary.bot.states.music import MusicMainSG
from idiotDiary.bot.states.not_working_place import NwpMainSG
from idiotDiary.bot.states.shaurma import FshPickFormSG
from idiotDiary.bot.states.start import MainMenuSG
from idiotDiary.bot.states.users import UserMainSG


@inject
async def main_menu_getter(event_from_user: User, **__):
    username = event_from_user.username or event_from_user.full_name
    return {"username": username}


main_menu = Dialog(
    Window(
        Format("{username}, куда надо?"),
        Column(
            Start(
                Const("нерабочая площадка 😶‍🌫️"),
                id="not_working_place",
                state=NwpMainSG.state,
                when=F_User.roles.contains("nwp")
            ),
            Start(
                Const("(бес)платная шаурма 🌯"),
                id="free_shaurma",
                state=FshPickFormSG.device,
                when=F_User.roles.contains("shaurma")
            ),
            Start(
                Const("напоминальщик ДР 🎂"),
                id="birthdays",
                state=BirthdaysMenuSG.state,
                when=F_User.roles.contains("birthdays")
            ),
            Start(
                Const("Музыка 🎧"),
                id="music",
                state=MusicMainSG.state
            ),
            Start(
                Const("Профиль 👤"),
                id="user_profile",
                state=UserMainSG.state,
            ),
            Start(
                Const("Админка ⚙️"),
                id="admin",
                state=AdminMainSG.state,
                when=F_User.is_superuser
            ),
        ),
        getter=main_menu_getter,
        state=MainMenuSG.state,
    ),
    launch_mode=LaunchMode.ROOT
)
