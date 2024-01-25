from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apps.birthdays.scheduler import send_birthdays, get_birthday_job_id
from apps.birthdays.ORM.notifications import NotificationUser
from config import settings

scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)


async def init_schedules(bot: Bot):
    notification_users = await NotificationUser.get_all()
    for notification_user in notification_users:
        for notification_time in notification_user.times:
            scheduler.add_job(
                func=send_birthdays,
                id=get_birthday_job_id(notification_user.user_id, notification_time.time),
                trigger="cron",
                hour=(notification_time.time.hour + notification_user.timeshift.hour) % 24,
                minute=(notification_time.time.minute + notification_user.timeshift.minute) % 60,
                kwargs={
                    "bot": bot,
                    "user_id": notification_user.user_id
                },
            )
