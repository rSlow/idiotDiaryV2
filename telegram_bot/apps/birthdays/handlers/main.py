from datetime import timedelta, date

from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Start, Column
from aiogram_dialog.widgets.text import Const
from sqlalchemy.ext.asyncio import AsyncSession

from common.buttons import MAIN_MENU_BUTTON
from common.utils.functions import get_now
from ..ORM.birthdays import Birthday
from ..states import BirthdaysFSM, ClearBirthdaysFSM, TimeCorrectionFSM, BirthdaysNotificationFSM
from ..utils.render import render_check_birthdays


async def get_birthdays_text(session: AsyncSession,
                             user_id: int):
    today = get_now().date()
    birthdays = await Birthday.get_birthdays_in_dates(
        session=session,
        user_id=user_id,
        start_date=today,
        end_date=today + timedelta(days=4)
    )
    dates: dict[date, list[Birthday]] = {}
    for birthday in birthdays:
        dates.setdefault(date(
            day=birthday.date.day,
            month=birthday.date.month,
            year=today.year
        ), []).append(birthday)

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
