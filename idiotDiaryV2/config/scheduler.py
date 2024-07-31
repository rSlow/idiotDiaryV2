from datetime import time
from typing import Sequence

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apps.birthdays.ORM.notifications import NotificationUser, NotificationTime
from apps.birthdays.scheduler import send_birthdays


class NotificationScheduler(AsyncIOScheduler):
    async def init(self, bot: Bot) -> None:
        notification_users = await NotificationUser.get_all()
        for notification_user in notification_users:
            for notification_time in notification_user.times:
                self.add_job(
                    func=send_birthdays,
                    id=self.get_birthday_job_id(notification_user.user_id, notification_time.time),
                    trigger="cron",
                    hour=(notification_time.time.hour + notification_user.timeshift.hour) % 24,
                    minute=(notification_time.time.minute + notification_user.timeshift.minute) % 60,
                    kwargs={
                        "bot": bot,
                        "user_id": notification_user.user_id
                    },
                )

    async def update_schedules(self,
                               notifications: Sequence[NotificationTime],
                               user_id: int,
                               timeshift: time,
                               bot: Bot):
        for notification in notifications:
            self.remove_birthday_job(
                user_id=notification.user_id,
                t=notification.time
            )
            self.add_birthday_job(
                user_id=user_id,
                t=notification.time,
                timeshift=timeshift,
                bot=bot
            )

    @staticmethod
    def get_birthday_job_id(user_id: int,
                            t: time):
        job_id = str(hash((user_id, t)))
        return job_id

    def add_birthday_job(self,
                         user_id: int,
                         t: time,
                         timeshift: time,
                         bot: Bot):
        self.add_job(
            func=send_birthdays,
            id=self.get_birthday_job_id(user_id, t),
            trigger="cron",
            hour=(t.hour + timeshift.hour) % 24,
            minute=(t.minute + timeshift.minute) % 60,
            kwargs={
                "bot": bot,
                "user_id": user_id
            }
        )

    def remove_birthday_job(self,
                            user_id: int,
                            t: time):
        self.remove_job(
            job_id=self.get_birthday_job_id(user_id, t)
        )
