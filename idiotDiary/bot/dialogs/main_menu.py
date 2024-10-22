from aiogram.types import User
from aiogram_dialog import Dialog, Window, LaunchMode
from aiogram_dialog.widgets.text import Format

from idiotDiary.bot.states.start import MainMenuSG


async def username_getter(event_from_user: User, **__):
    return {'username': event_from_user.username or event_from_user.full_name}


main_menu = Dialog(
    Window(
        Format("{username}, куда надо?"),
        # Column(
        #     Start(
        #         Const("нерабочая площадка 😶‍🌫️"),
        #         id="not_working_place",
        #         state=NWPStartFSM.state
        #     ),
        #     Start(
        #         Const("(бес)платная шаурма 🌯"),
        #         id="free_shaurma",
        #         state=FShStartFSM.device
        #     ),
        #     Start(
        #         Const("напоминальщик ДР 🎂"),
        #         id="birthdays",
        #         state=BirthdaysFSM.state,
        #         when=WhenBirthdays()
        #     ),
        #     Start(
        #         Const("Музыка 🎧"),
        #         id="music",
        #         state=MusicMainFSM.state
        #     ),
        #     Start(
        #         Const("Админка ⚙️"),
        #         id="admin",
        #         state=AdminFSM.state,
        #         when=filters.adg_is_superuser
        #     ),
        # ),
        getter=username_getter,
        state=MainMenuSG.state,
    ),
    launch_mode=LaunchMode.ROOT
)
