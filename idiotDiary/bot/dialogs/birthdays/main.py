from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Start, Column
from aiogram_dialog.widgets.text import Const
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from idiotDiary.bot.di.jinja import JinjaRenderer
from idiotDiary.bot.states.birthdays import (
    TimeCorrectionSG, ClearBirthdaysSG, BirthdaysNotificationSG, CalendarSG,
    BirthdaysMenuSG
)
from idiotDiary.bot.views import buttons as b
from idiotDiary.bot.views.birthdays import get_birthdays_message
from idiotDiary.core.db import dto
from idiotDiary.core.db.dao.birthday import BirthdayDao


@inject
async def check_birthdays_callback(
        callback: types.CallbackQuery, _, manager: DialogManager,
        dao: FromDishka[BirthdayDao], jinja: FromDishka[JinjaRenderer]
):
    user: dto.User = manager.middleware_data["user"]
    message_text = await get_birthdays_message(dao, user.id_, jinja)
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await callback.message.answer(message_text)


main_birthday_dialog = Dialog(
    Window(
        Const("Выберите действие:"),
        Column(
            Button(
                Const("Проверить ДР 🎈"),
                id="check",
                on_click=check_birthdays_callback  # noqa
            ),
            Start(
                Const("Календарь 📆"),
                id="calendar",
                state=CalendarSG.state
            ),
            Start(
                Const("Оповещения 🕓"),
                id="notifications",
                state=BirthdaysNotificationSG.state
            ),
            Start(
                Const("Очистить данные 🗑"),
                id="clear_data",
                state=ClearBirthdaysSG.state
            ),
            Start(
                Const("Установка часового пояса 🌏"),
                id="time_correction",
                state=TimeCorrectionSG.state
            ),
            b.MAIN_MENU,
        ),
        state=BirthdaysMenuSG.state
    )
)
