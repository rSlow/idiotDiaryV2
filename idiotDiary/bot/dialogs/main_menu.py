from aiogram import F
from aiogram.types import User
from aiogram_dialog import Dialog, Window, LaunchMode
from aiogram_dialog.widgets.kbd import Column, Start
from aiogram_dialog.widgets.text import Format, Const
from dishka.integrations.aiogram_dialog import inject

from idiotDiary.bot.states.not_working_place import NwpMainSG
from idiotDiary.bot.states.start import MainMenuSG
from idiotDiary.core.data.db import dto


@inject
async def main_menu_getter(event_from_user: User, user: dto.User, **__):
    username = event_from_user.username or event_from_user.full_name
    user_roles: list[str] = getattr(user, "roles", [])
    return {
        "username": username,
        "user_roles": user_roles
    }


main_menu = Dialog(
    Window(
        Format("{username}, куда надо?"),
        Column(
            Start(
                Const("нерабочая площадка 😶‍🌫️"),
                id="not_working_place",
                state=NwpMainSG.state,
                when=F["nwp"].in_(F["user_roles"])
            ),
            # Start(
            #     Const("(бес)платная шаурма 🌯"),
            #     id="free_shaurma",
            #     state=FShStartFSM.device
            # ),
            # Start(
            #     Const("напоминальщик ДР 🎂"),
            #     id="birthdays",
            #     state=BirthdaysFSM.state,
            #     when=WhenBirthdays()
            # ),
            # Start(
            #     Const("Музыка 🎧"),
            #     id="music",
            #     state=MusicMainFSM.state
            # ),
            # Start(
            #     Const("Админка ⚙️"),
            #     id="admin",
            #     state=AdminFSM.state,
            #     when=filters.adg_is_superuser
            # ),
        ),
        getter=main_menu_getter,
        state=MainMenuSG.state,
    ),
    launch_mode=LaunchMode.ROOT
)
