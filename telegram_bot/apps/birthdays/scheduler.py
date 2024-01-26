from datetime import timedelta

from aiogram import Bot

from common.ORM.database import Session
from common.utils.functions import get_now
from .ORM.birthdays import Birthday
from .utils.render import render_schedule_birthdays


async def send_birthdays(bot: Bot, user_id: int):
    today = get_now()
    async with Session() as session:
        today_birthdays = await Birthday.get_birthdays_in_date(
            session=session,
            user_id=user_id,
            d=today
        )
        tomorrow_birthdays = await Birthday.get_birthdays_in_date(
            session=session,
            user_id=user_id,
            d=today + timedelta(days=1)
        )
        if today_birthdays or tomorrow_birthdays:
            message_text = render_schedule_birthdays(
                today_birthdays=today_birthdays,
                tomorrow_birthdays=tomorrow_birthdays
            )
            await bot.send_message(
                chat_id=user_id,
                text=message_text
            )
