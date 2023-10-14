from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apps.not_working_place.schedules import send_birthdays
from config import settings

scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)


def init_schedules(bot: Bot):
    scheduler.add_job(
        func=send_birthdays,
        trigger="cron",
        hour=10,
        minute=00,
        kwargs={
            "bot": bot
        }
    )