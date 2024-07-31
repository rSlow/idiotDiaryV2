from datetime import time

from aiogram import types, Bot
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from sqlalchemy.ext.asyncio import AsyncSession

from common.dialogs.types import JinjaTemplate
from common.buttons import CANCEL_BUTTON
from config import formats
from config.scheduler import NotificationScheduler
from ..states import TimeCorrectionFSM
from ..ORM.notifications import NotificationUser, NotificationTime
from ..filters import TimeValidFactory
from ..utils.timeshift import get_timeshift
from .. import settings as birthdays_settings


async def success_handler(message: types.Message,
                          _: ManagedTextInput,
                          manager: DialogManager,
                          valid_time: time):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    middleware_data = manager.middleware_data
    session: AsyncSession = middleware_data["session"]
    user_id: int = middleware_data["user_id"]
    scheduler: NotificationScheduler = middleware_data["scheduler"]
    bot: Bot = middleware_data["bot"]

    timeshift = get_timeshift(valid_time)
    await NotificationUser.add_or_update_user(
        session=session,
        user_id=user_id,
        timeshift=timeshift
    )
    notifications = await NotificationTime.get_notifications(
        session=session,
        user_id=user_id
    )
    await scheduler.update_schedules(
        notifications=notifications,
        user_id=user_id,
        timeshift=timeshift,
        bot=bot
    )

    await message.answer(f"Часовой пояс c временем {valid_time:{formats.TIME_FORMAT}} сохранен.")
    await manager.done()


async def error_handler(message: types.Message,
                        _: ManagedTextInput,
                        manager: DialogManager,
                        __: ValueError):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.answer(f"Введен неверный формат времени. Попробуйте еще раз.")


time_correction_dialog = Dialog(
    Window(
        JinjaTemplate(
            template_name="time_correction.jinja2",
            templates_dir=birthdays_settings.TEMPLATES_DIR
        ),
        TextInput(
            id="timeshift",
            type_factory=TimeValidFactory(),
            on_success=success_handler,
            on_error=error_handler
        ),
        CANCEL_BUTTON,
        state=TimeCorrectionFSM.state
    )
)
