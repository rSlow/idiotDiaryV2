from datetime import timedelta, time

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from common.ORM.database import Session
from common.utils.functions import get_now
from .ORM.birthdays import Birthday
from .utils.render import render_schedule_birthdays


def get_birthday_job_id(user_id: int,
                        t: time):
    job_id = str(hash((user_id, t)))
    return job_id


def add_birthday_job(scheduler: AsyncIOScheduler,
                     user_id: int,
                     t: time,
                     timeshift: time,
                     bot: Bot):
    scheduler.add_job(
        func=send_birthdays,
        id=get_birthday_job_id(user_id, t),
        trigger="cron",
        hour=(t.hour + timeshift.hour) % 24,
        minute=(t.minute + timeshift.minute) % 60,
        kwargs={
            "bot": bot,
            "user_id": user_id
        }
    )


def remove_birthday_job(scheduler: AsyncIOScheduler,
                        user_id: int,
                        t: time):
    scheduler.remove_job(
        job_id=get_birthday_job_id(user_id, t)
    )


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
