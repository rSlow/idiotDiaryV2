from datetime import timedelta, date
from typing import Sequence

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from common.FSM import CommonFSM
from common.filters import NoKeyboardFilter, YesKeyboardFilter, BackFilter
from common.keyboards.base import YesNoKeyboard
from common.keyboards.start import StartKeyboard
from common.utils.functions import get_now
from ..FSM.main import BirthdaysFSM, TimeCorrectionFSM
from ..ORM.birthdays import Birthday
from ..keyboards.main import BirthdaysMainKeyboard
from ..utils.render import render_check_birthdays

main_birthday_router = Router(name="main_birthdays")


@main_birthday_router.message(
    CommonFSM.start,
    F.text == StartKeyboard.Buttons.birthdays,
)
@main_birthday_router.message(
    BirthdaysFSM.clear_confirm,
    NoKeyboardFilter(),
)
@main_birthday_router.message(
    TimeCorrectionFSM.start,
    BackFilter(),
)
async def main_birthdays(message: types.Message,
                         state: FSMContext):
    await state.set_state(BirthdaysFSM.main)
    await message.answer(
        text="Выберите действие:",
        reply_markup=BirthdaysMainKeyboard.build()
    )


@main_birthday_router.message(
    Command("birthdays"),
)
@main_birthday_router.message(
    BirthdaysFSM.main,
    F.text == BirthdaysMainKeyboard.Buttons.check,
)
async def check_birthdays(message: types.Message,
                          user_id: int,
                          session: AsyncSession):
    today = get_now().date()
    dates: dict[date, Sequence[Birthday]] = {}
    for i in range(4):
        check_date = today + timedelta(days=i)
        date_list = await Birthday.get_birthdays_in_date(
            session=session,
            user_id=user_id,
            d=check_date
        )
        if date_list:
            dates[check_date] = date_list

    message_text = render_check_birthdays(dates)
    await message.answer(message_text)


@main_birthday_router.message(
    BirthdaysFSM.main,
    F.text == BirthdaysMainKeyboard.Buttons.clear_data,
)
async def confirm_clear_birthdays(message: types.Message,
                                  state: FSMContext):
    await state.set_state(BirthdaysFSM.clear_confirm)

    await message.answer(
        text="Вы уверены?",
        reply_markup=YesNoKeyboard.build()
    )


@main_birthday_router.message(
    BirthdaysFSM.clear_confirm,
    YesKeyboardFilter(),
)
async def clear_birthdays(message: types.Message,
                          state: FSMContext,
                          user_id: int,
                          session: AsyncSession):
    await Birthday.delete_data(
        user_id=user_id,
        session=session
    )

    await message.answer(
        text="Все дни рождения удалены.",
    )

    await main_birthdays(
        message=message,
        state=state
    )
