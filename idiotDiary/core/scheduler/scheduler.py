import logging
from asyncio import Protocol

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import AsyncContainer
from redis import Redis

from idiotDiary.core.config.models.redis import RedisConfig
from idiotDiary.core.db import dto
from idiotDiary.core.scheduler.context import SchedulerInjectContext

logger = logging.getLogger(__name__)


class Scheduler(Protocol):
    async def start(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def __aenter__(self):
        logger.info("Starting scheduler")
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class ApScheduler(Scheduler):
    def __init__(self, dishka: AsyncContainer, redis_config: RedisConfig):
        # TODO move to di
        SchedulerInjectContext.container = dishka
        self.job_store = RedisJobStore(
            host=redis_config.host,
            port=redis_config.port,
            db=redis_config.db,
            password=redis_config.password
        )
        self.job_store.redis = Redis.from_url(redis_config.uri)
        self.executor = AsyncIOExecutor()
        job_defaults = {  # TODO check
            "coalesce": False,
            "max_instances": 20,
            "misfire_grace_time": 3600,
        }
        logger.info("configuring shedulder...")
        self.scheduler = AsyncIOScheduler(
            jobstores={"default": self.job_store},
            job_defaults=job_defaults,
            executors={"default": self.executor},
        )

    async def start(self):
        # TODO scheduler не стартует (выдается только в middleware data,
        #  нужно запускать самостоятельно)
        self.scheduler.start()

    async def close(self):
        self.scheduler.shutdown()
        self.executor.shutdown()
        self.job_store.shutdown()

    # ----- TASKS -----#
    def remove_birthday_notification(
            self, notification: dto.NotificationTime
    ):
        job_id = _prepare_notification_key(notification)
        try:
            self.scheduler.remove_job(job_id=job_id)
        except JobLookupError as e:
            logger.error(
                "can't remove job %s for preparing game %s",
                job_id,
                notification.id_,
                exc_info=e,
            )

    def add_birthday_notification(
            self, notification: dto.NotificationTime,
            state: dto.NotificationState
    ):

        self.scheduler.add_job(
            func="idiotDiary.core.scheduler.tasks:"
                 "send_birthdays",
            id=_prepare_notification_key(notification),
            trigger="cron",
            hour=(notification.time.hour + state.timeshift.hour) % 24,
            minute=(notification.time.minute + state.timeshift.minute) % 60,
            kwargs={"user_id": state.user_id}
        )

    def update_user_birthdays(
            self, state: dto.NotificationState,
            notifications: list[dto.NotificationTime]
    ):
        for notification in notifications:
            self.remove_birthday_notification(notification)
            self.add_birthday_notification(notification, state)


def _prepare_notification_key(notification: dto.NotificationTime) -> str:
    return f"notification-{notification.id_}"
