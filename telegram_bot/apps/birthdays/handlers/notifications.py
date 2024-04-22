from datetime import time
from operator import itemgetter

from aiogram import types, Bot
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Column, Start, Button, Select
from aiogram_dialog.widgets.text import Const, Format
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from common.dialogs.types import JinjaTemplate
from common.buttons import CANCEL_BUTTON
from common.utils.functions import get_now
from common.dialogs import yes_no_dialog_factory
from config import formats
from config.scheduler import NotificationScheduler
from ..filters import TimeValidFactory
from ..states import BirthdaysNotificationFSM, ClearNotificationFSM, AddNotificationTimeFSM
from ..ORM.notifications import NotificationTime, NotificationUser
from .. import settings as birthdays_settings


async def main_getter(session: AsyncSession,
                      user_id: int,
                      **__):
    notifications = await NotificationTime.get_notifications(
        session=session,
        user_id=user_id
    )
    template_times = [notification.time for notification in notifications]
    buttons_times = [(f"{_time:{formats.TIME_FORMAT}} ❌", f"{_time:{formats.TIME_FORMAT}}")
                     for _time in template_times]
    return {
        "times": template_times,
        "buttons_times": buttons_times
    }


async def delete_notification(callback: types.CallbackQuery,
                              _: Button,
                              manager: DialogManager,
                              button_time: str):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    middleware_data = manager.middleware_data
    session: AsyncSession = middleware_data["session"]
    user_id: int = middleware_data["user_id"]
    scheduler: NotificationScheduler = middleware_data["scheduler"]
    valid_time: time = TimeValidFactory()(button_time)
    try:
        await NotificationTime.delete_notification(
            user_id=user_id,
            session=session,
            notification_time=valid_time
        )
        scheduler.remove_birthday_job(
            user_id=user_id,
            t=valid_time
        )
        await callback.message.answer(f"Время оповещения {valid_time:{formats.TIME_FORMAT}} удалено.")
    except NoResultFound:
        pass


notifications_dialog = Dialog(
    Window(
        JinjaTemplate(
            template_name="notifications.jinja2",
            templates_dir=birthdays_settings.TEMPLATES_DIR
        ),
        Select(
            Format('{item[0]}'),
            id='times',
            item_id_getter=itemgetter(1),
            items='buttons_times',
            on_click=delete_notification
        ),
        Column(
            Start(
                Const("Добавить время ➕"),
                id="add_time",
                state=AddNotificationTimeFSM.state
            ),
            Start(
                Const("Очистить все 🗑"),
                id="clear",
                state=ClearNotificationFSM.state
            ),
            CANCEL_BUTTON,
        ),
        getter=main_getter,
        state=BirthdaysNotificationFSM.state
    )
)


async def clear_notifications(callback: types.CallbackQuery,
                              _: Button,
                              manager: DialogManager):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    middleware_data = manager.middleware_data
    session: AsyncSession = middleware_data["session"]
    user_id: int = middleware_data["user_id"]
    scheduler: NotificationScheduler = middleware_data["scheduler"]

    notifications = await NotificationTime.get_notifications(
        session=session,
        user_id=user_id
    )
    await session.close()
    await NotificationTime.clear_notifications(
        user_id=user_id,
        session=session
    )
    for notification in notifications:
        scheduler.remove_birthday_job(
            user_id=user_id,
            t=notification.time
        )
    await callback.message.answer("Все настройки оповещений удалены.")
    await manager.done()


clear_notifications_dialog = yes_no_dialog_factory(
    Const("Полная очистка оповещений. Вы уверены?"),
    state=ClearNotificationFSM.state,
    on_click=clear_notifications
)


async def success_time_add_handler(message: types.Message,
                                   _: ManagedTextInput,
                                   manager: DialogManager,
                                   valid_time: time):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    middleware_data = manager.middleware_data
    session: AsyncSession = middleware_data["session"]
    user_id: int = middleware_data["user_id"]
    scheduler: NotificationScheduler = middleware_data["scheduler"]
    bot: Bot = middleware_data["bot"]

    await NotificationTime.add_notification(
        session=session,
        user_id=user_id,
        notification_time=valid_time,
    )
    user = await NotificationUser.get_user(
        session=session,
        user_id=user_id
    )
    scheduler.add_birthday_job(
        user_id=user_id,
        t=valid_time,
        bot=bot,
        timeshift=user.timeshift,
    )
    await message.answer(f"Время {valid_time:{formats.TIME_FORMAT}} добавлено.")
    await manager.done()


async def error_time_add_handler(message: types.Message,
                                 _: ManagedTextInput,
                                 manager: DialogManager,
                                 __: ValueError):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.answer("Неверный формат времени. Попробуйте еще раз.")


add_time_notification_dialog = Dialog(
    Window(
        Const("Введите время в формате ЧЧ:ММ"),
        Const(f"Например: {get_now().time():{formats.TIME_FORMAT}}"),
        TextInput(
            id="time_to_add",
            type_factory=TimeValidFactory(),
            on_success=success_time_add_handler,
            on_error=error_time_add_handler
        ),
        CANCEL_BUTTON,
        state=AddNotificationTimeFSM.state,
    )
)
