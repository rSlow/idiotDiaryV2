from aiogram import types
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from sqlalchemy.ext.asyncio import AsyncSession

from apps.birthdays.ORM.birthdays import Birthday
from apps.birthdays.states import ClearBirthdaysFSM
from common.dialogs import yes_no_dialog_factory


async def clear_birthdays(callback: types.CallbackQuery,
                          _: Button,
                          manager: DialogManager):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    session: AsyncSession = manager.middleware_data["session"]
    user_id: int = manager.middleware_data["user_id"]

    await Birthday.delete_data(
        user_id=user_id,
        session=session
    )

    await callback.message.answer("Все дни рождения удалены.")
    await manager.done()


clear_dialog = yes_no_dialog_factory(
    Const("Очистка всех данных о днях рождения."),
    Const("Вы уверены?"),
    state=ClearBirthdaysFSM.state,
    on_click=clear_birthdays
)
