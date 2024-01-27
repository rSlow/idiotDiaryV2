from datetime import time

from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from common.keyboards.base import BackKeyboard
from config import formats
from config.scheduler import NotificationScheduler
from .check_birthdays import main_birthdays
from ..FSM.main import BirthdaysFSM, TimeCorrectionFSM
from ..ORM.notifications import NotificationUser, NotificationTime
from ..filters import TimeValidFilter, TimeNotValidFilter
from ..keyboards.main import BirthdaysMainKeyboard
from ..utils.render import render_time_correction
from ..utils.timeshift import get_timeshift

time_correction_router = Router(name="time_correction")


@time_correction_router.message(
    BirthdaysFSM.main,
    F.text == BirthdaysMainKeyboard.Buttons.time_correction,
)
async def wait_current_user_time(message: types.Message,
                                 state: FSMContext):
    await state.set_state(TimeCorrectionFSM.start)
    message_text = render_time_correction()
    await message.answer(
        text=message_text,
        reply_markup=BackKeyboard.build()
    )


@time_correction_router.message(
    TimeCorrectionFSM.start,
    TimeValidFilter(),
)
async def set_current_user_time(message: types.Message,
                                state: FSMContext,
                                valid_time: time,
                                session: AsyncSession,
                                user_id: int,
                                scheduler: NotificationScheduler,
                                bot: Bot):
    await state.set_state(TimeCorrectionFSM.set)
    timeshift = get_timeshift(valid_time)
    await NotificationUser.add_or_update_user(
        session=session,
        user_id=user_id,
        timeshift=timeshift
    )

    await message.answer(f"Часовой пояс c временем {valid_time:{formats.TIME_FORMAT}} сохранен.")

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

    await main_birthdays(
        message=message,
        state=state
    )


@time_correction_router.message(
    TimeCorrectionFSM.start,
    TimeNotValidFilter(),
)
async def set_current_user_time(message: types.Message):
    await message.answer(f"Введен неверный формат времени. Попробуйте еще раз.")
