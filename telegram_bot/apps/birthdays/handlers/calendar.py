from datetime import date

from aiogram.types import User
from aiogram_dialog import Window, Dialog, DialogManager, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import ManagedCalendar
from aiogram_dialog.widgets.text import Const
from sqlalchemy.ext.asyncio import AsyncSession

from common.buttons import CANCEL_BUTTON
from common.dialogs.types import LocalizedCalendar
from ..ORM.birthdays import Birthday
from ..states import CalendarFSM
from ..utils.render import render_check_birthdays


async def on_date_selected(callback: ChatEvent,
                           _: ManagedCalendar,
                           manager: DialogManager,
                           selected_date: date):
    session: AsyncSession = manager.middleware_data["session"]
    user: User = manager.middleware_data["event_from_user"]
    birthdays = await Birthday.get_birthdays_in_date(
        session=session,
        user_id=user.id,
        d=selected_date
    )
    if birthdays:
        message_text = render_check_birthdays({selected_date: birthdays})
        manager.show_mode = ShowMode.DELETE_AND_SEND
        await callback.message.answer(message_text)
    else:
        await callback.answer("Нет дней рождения.")


calendar_dialog = Dialog(
    Window(
        Const("Выберите дату для проверки:"),
        LocalizedCalendar(
            id="cal",
            on_click=on_date_selected,
        ),
        CANCEL_BUTTON,
        state=CalendarFSM.state
    )
)
