from datetime import time

from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from common.filters import YesKeyboardFilter, NoKeyboardFilter
from common.keyboards.base import YesNoKeyboard, CancelKeyboard
from common.utils.functions import get_now
from config import formats
from config.scheduler import NotificationScheduler
from ..FSM.main import BirthdaysFSM, BirthdaysNotificationFSM
from ..ORM.notifications import NotificationTime, NotificationUser
from ..filters import TimeValidFilter, TimeNotValidFilter
from ..keyboards.main import BirthdaysMainKeyboard
from ..keyboards.notifications import BirthdaysNotificationsKeyboard
from ..utils.render import render_notifications

notifications_router = Router(name="notifications_birthdays")


@notifications_router.message(
    BirthdaysFSM.main,
    F.text == BirthdaysMainKeyboard.Buttons.notifications,
)
@notifications_router.message(
    BirthdaysNotificationFSM.clear,
    NoKeyboardFilter(),
)
async def main_notifications(message: types.Message,
                             state: FSMContext,
                             user_id: int,
                             session: AsyncSession):
    await state.set_state(BirthdaysNotificationFSM.main)
    notifications = await NotificationTime.get_notifications(
        session=session,
        user_id=user_id
    )
    message_text = render_notifications(notifications)
    await message.answer(
        text=message_text,
        reply_markup=BirthdaysNotificationsKeyboard.build(
            notifications=notifications
        )
    )


@notifications_router.message(
    BirthdaysNotificationFSM.main,
    F.text == BirthdaysNotificationsKeyboard.Buttons.add,
)
async def add_time_notification(message: types.Message,
                                state: FSMContext):
    await state.set_state(BirthdaysNotificationFSM.add_time)
    await message.answer(
        text=f"Введите время в формате ЧЧ:ММ \n"
             f"Например: {get_now().time():{formats.TIME_FORMAT}}",
        reply_markup=CancelKeyboard.build()
    )


@notifications_router.message(
    BirthdaysNotificationFSM.add_time,
    TimeValidFilter(),
)
async def valid_add_time_notification(message: types.Message,
                                      state: FSMContext,
                                      user_id: int,
                                      valid_time: time,
                                      session: AsyncSession,
                                      scheduler: NotificationScheduler,
                                      bot: Bot):
    await state.set_state(BirthdaysNotificationFSM.confirm_add_time)
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
    await main_notifications(
        message=message,
        state=state,
        user_id=user_id,
        session=session
    )


@notifications_router.message(
    BirthdaysNotificationFSM.add_time,
    TimeNotValidFilter(),
)
async def invalid_add_time_notification(message: types.Message):
    await message.answer("Неверный формат времени. Попробуйте еще раз.")


@notifications_router.message(
    BirthdaysNotificationFSM.main,
    F.text == BirthdaysNotificationsKeyboard.Buttons.clear,
)
async def clear_notifications(message: types.Message,
                              state: FSMContext):
    await state.set_state(BirthdaysNotificationFSM.clear)
    await message.answer(
        text="Полная очистка оповещений. Вы уверены?",
        reply_markup=YesNoKeyboard.build()
    )


@notifications_router.message(
    BirthdaysNotificationFSM.clear,
    YesKeyboardFilter(),
)
async def clear_confirm_notifications(message: types.Message,
                                      state: FSMContext,
                                      user_id: int,
                                      session: AsyncSession,
                                      scheduler: NotificationScheduler):
    notifications = await NotificationTime.get_notifications(
        session=session,
        user_id=user_id
    )
    await NotificationTime.clear_notifications(
        user_id=user_id,
        session=session
    )
    for notification in notifications:
        scheduler.remove_birthday_job(
            user_id=user_id,
            t=notification.time
        )
    await message.answer("Все настройки оповещений удалены.")
    await main_notifications(
        message=message,
        state=state,
        user_id=user_id,
        session=session,
    )


@notifications_router.message(
    BirthdaysNotificationFSM.main,
    TimeValidFilter(),
)
async def delete_notification(message: types.Message,
                              state: FSMContext,
                              user_id: int,
                              session: AsyncSession,
                              valid_time: time,
                              scheduler: NotificationScheduler):
    await state.set_state(BirthdaysNotificationFSM.del_time)
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
        await message.answer(f"Время оповещения {valid_time:{formats.TIME_FORMAT}} удалено.")
        await main_notifications(
            message=message,
            state=state,
            user_id=user_id,
            session=session,
        )
    except NoResultFound:
        await message.delete()
        await state.set_state(BirthdaysNotificationFSM.main)
