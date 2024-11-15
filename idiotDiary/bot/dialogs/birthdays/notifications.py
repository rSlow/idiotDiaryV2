from datetime import time

from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Column, Start, Select
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from idiotDiary.bot.states.birthdays import AddNotificationTimeSG, \
    ClearNotificationSG, BirthdaysNotificationSG
from idiotDiary.bot.utils.dialog_factory import choice_dialog_factory
from idiotDiary.bot.utils.input_validation import error_dt_input_handler, \
    time_from_text
from idiotDiary.bot.views import buttons as b
from idiotDiary.bot.views.types import JinjaTemplate
from idiotDiary.core.db import dto
from idiotDiary.core.db.dao.notification import UserNotificationDao
from idiotDiary.core.scheduler.scheduler import ApScheduler
from idiotDiary.core.utils import dates
from idiotDiary.core.utils.dates import get_now


@inject
async def main_getter(
        user: dto.User, note_dao: FromDishka[UserNotificationDao], **__
):
    notifications = await note_dao.get_user_notifications(user_id=user.id_)
    notification_values = [
        (
            notification,
            f"❌ {notification.time:{dates.TIME_FORMAT}}"
        )
        for notification in notifications
    ]
    return {"notifications": notification_values}


@inject
async def delete_notification(
        callback: types.CallbackQuery, _, manager: DialogManager,
        notification_id: str, dao: FromDishka[UserNotificationDao],
        scheduler: FromDishka[ApScheduler]
):
    notification_id = int(notification_id)
    notification = await dao.get_notification(notification_id)
    await dao.delete_notification(notification_id)
    scheduler.remove_birthday_notification(notification)
    await callback.message.answer(
        f"Время оповещения {notification.time:{dates.TIME_FORMAT}} удалено."
    )
    manager.show_mode = ShowMode.DELETE_AND_SEND


notifications_dialog = Dialog(
    Window(
        JinjaTemplate("birthdays/notifications.jinja2"),
        Select(
            Format("{item[1]}"),
            id="notifications",
            item_id_getter=lambda n: n[0].id_,
            items="notifications",
            on_click=delete_notification  # noqa
        ),
        Column(
            Start(
                Const("Добавить время ➕"),
                id="add_time",
                state=AddNotificationTimeSG.state
            ),
            Start(
                Const("Очистить все 🗑"),
                id="clear",
                state=ClearNotificationSG.state
            ),
            b.CANCEL,
        ),
        getter=main_getter,
        state=BirthdaysNotificationSG.state
    )
)


@inject
async def clear_notifications(
        callback: types.CallbackQuery, _, manager: DialogManager,
        dao: FromDishka[UserNotificationDao], scheduler: FromDishka[ApScheduler]
):
    user: dto.User = manager.middleware_data["user"]
    notifications = await dao.get_user_notifications(user_id=user.id_)
    await dao.clear_notifications(user_id=user.id_)
    for notification in notifications:
        scheduler.remove_birthday_notification(notification)

    await callback.message.answer("Все настройки оповещений удалены.")
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


clear_notifications_dialog = choice_dialog_factory(
    Const("Полная очистка оповещений. Вы уверены?"),
    state=ClearNotificationSG.state,
    on_click=clear_notifications  # noqa
)


@inject
async def success_time_add_handler(
        message: types.Message, _, manager: DialogManager, valid_time: time,
        dao: FromDishka[UserNotificationDao], scheduler: FromDishka[ApScheduler]
):
    user: dto.User = manager.middleware_data["user"]
    notification = await dao.add_notification(
        user_id=user.id_, notification_time=valid_time
    )
    user_state = await dao.get_user_state(user.id_)
    scheduler.add_birthday_notification(notification, user_state)

    await message.answer(f"Время {valid_time:{dates.TIME_FORMAT}} добавлено.")
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


add_time_notification_dialog = Dialog(
    Window(
        Const(f"Введите время в формате {dates.TIME_FORMAT_USER}"),
        Const(f"Например: {get_now():{dates.TIME_FORMAT}}"),
        TextInput(
            id="time_to_add",
            type_factory=time_from_text,
            on_success=success_time_add_handler,  # noqa
            on_error=error_dt_input_handler
        ),
        b.CANCEL,
        state=AddNotificationTimeSG.state,
    )
)