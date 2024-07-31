from datetime import timedelta, date
from typing import Sequence

from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Start, Column
from aiogram_dialog.widgets.text import Const
from sqlalchemy.ext.asyncio import AsyncSession

from common.buttons import MAIN_MENU_BUTTON
from common.utils.functions import get_now
from ..ORM.birthdays import Birthday
from ..states import BirthdaysFSM, ClearBirthdaysFSM, TimeCorrectionFSM, BirthdaysNotificationFSM, CalendarFSM
from ..utils.render import render_check_birthdays


async def get_birthdays_text(session: AsyncSession,
                             user_id: int):
    today = get_now().date()
    dates: dict[date, Sequence[Birthday]] = {}
    for i in range(4):
        fetch_date = today + timedelta(days=i)
        birthdays = await Birthday.get_birthdays_in_date(
            session=session,
            user_id=user_id,
            d=fetch_date
        )
        if birthdays:
            dates[fetch_date] = birthdays

    message_text = render_check_birthdays(dates)
    return message_text


async def check_birthdays_callback(callback: types.CallbackQuery,
                                   _: Button,
                                   manager: DialogManager):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    session: AsyncSession = manager.middleware_data["session"]
    user_id: int = manager.middleware_data["user_id"]
    message_text = await get_birthdays_text(
        session=session,
        user_id=user_id
    )
    await callback.message.answer(message_text)


main_birthday_dialog = Dialog(
    Window(
        Const("Выберите действие:"),
        Column(
            Button(
                Const("Проверить ДР 🎈"),
                id="check",
                on_click=check_birthdays_callback
            ),
            Start(
                Const("Календарь 📆"),
                id="calendar",
                state=CalendarFSM.state
            ),
            Start(
                Const("Оповещения 🕓"),
                id="notifications",
                state=BirthdaysNotificationFSM.state
            ),
            Start(
                Const("Очистить данные 🗑"),
                id="clear_data",
                state=ClearBirthdaysFSM.state
            ),
            Start(
                Const("Установка часового пояса 🌏"),
                id="time_correction",
                state=TimeCorrectionFSM.state
            ),
            MAIN_MENU_BUTTON,
        ),
        state=BirthdaysFSM.state
    )
)
