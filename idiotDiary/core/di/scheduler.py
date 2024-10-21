from typing import AsyncIterable

from dishka import Provider, Scope, provide, AsyncContainer

from idiotDiary.core.config.models.redis import RedisConfig
from idiotDiary.core.scheduler.scheduler import Scheduler, ApScheduler


class SchedulerProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_scheduler(
            self, dishka: AsyncContainer, redis_config: RedisConfig
    ) -> AsyncIterable[Scheduler]:
        async with ApScheduler(
                dishka=dishka,
                redis_config=redis_config
        ) as scheduler:
            yield scheduler
