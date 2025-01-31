from aiogram_dialog import Dialog, Window, LaunchMode
from aiogram_dialog.widgets.kbd import Column, Start
from aiogram_dialog.widgets.text import Format, Const

from idiotDiary.bot.filters.user import F_User, adg_role_filter
from idiotDiary.bot.states.admin import AdminMainSG
from idiotDiary.bot.states.birthdays import BirthdaysMenuSG
from idiotDiary.bot.states.music import MusicMainSG
from idiotDiary.bot.states.not_working_place import NwpMainSG
from idiotDiary.bot.states.shaurma import FshPickFormSG
from idiotDiary.bot.states.start import MainMenuSG
from idiotDiary.bot.states.subs import SubsMainFSM
from idiotDiary.bot.states.users import UserMainSG
from idiotDiary.core.db import dto


async def main_menu_getter(user: dto.User, **__):
    return {"mention": user.short_mention}


main_menu = Dialog(
    Window(
        Format("{mention}, куда надо?"),
        Column(
            Start(
                Const("нерабочая площадка 😶‍🌫️"),
                id="not_working_place",
                state=NwpMainSG.state,
                when=adg_role_filter("nwp")
            ),
            Start(
                Const("(бес)платная шаурма 🌯"),
                id="free_shaurma",
                state=FshPickFormSG.device,
                when=adg_role_filter("shaurma")
            ),
            Start(
                Const("напоминальщик ДР 🎂"),
                id="birthdays",
                state=BirthdaysMenuSG.state,
                when=adg_role_filter("birthdays")
            ),
            Start(
                Const("Музыка 🎧"),
                id="music",
                state=MusicMainSG.state,
                when=adg_role_filter("music")
            ),
            Start(
                Const("Профиль 👤"),
                id="user_profile",
                state=UserMainSG.state,
            ),
            Start(
                Const("Подписки FarPost 📈"),
                id="subs",
                state=SubsMainFSM.state,
                when=adg_role_filter("subs")
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
