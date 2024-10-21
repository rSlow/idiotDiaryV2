import logging
from asyncio import Protocol

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import AsyncContainer
from redis import Redis

from idiotDiary.core.config.models.redis import RedisConfig
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

    # TODO create jobs

    # async def plain_prepare(self, game: dto.Game):
    #     self.scheduler.add_job(
    #         func="shvatka.infrastructure.scheduler.wrappers:prepare_game_wrapper",
    #         kwargs={"game_id": game.id, "author_id": game.author.id},
    #         trigger="date",
    #         run_date=game.prepared_at.astimezone(tz=tz_utc),
    #         timezone=tz_utc,
    #         id=_prepare_game_key(game),
    #     )
    #
    # async def plain_start(self, game: dto.Game):
    #     assert game.start_at
    #     self.scheduler.add_job(
    #         func="shvatka.infrastructure.scheduler.wrappers:start_game_wrapper",
    #         kwargs={"game_id": game.id, "author_id": game.author.id},
    #         trigger="date",
    #         run_date=game.start_at.astimezone(tz=tz_utc),
    #         timezone=tz_utc,
    #         id=_start_game_key(game),
    #     )
    #
    # async def cancel_scheduled_game(self, game: dto.Game):
    #     try:
    #         self.scheduler.remove_job(job_id=_prepare_game_key(game))
    #     except JobLookupError as e:
    #         logger.error(
    #             "can't remove job %s for preparing game %s",
    #             _prepare_game_key(game),
    #             game.id,
    #             exc_info=e,
    #         )
    #     try:
    #         self.scheduler.remove_job(job_id=_start_game_key(game))
    #     except JobLookupError as e:
    #         logger.error(
    #             "can't remove job %s for start game %s",
    #             _start_game_key(game), game.id,
    #             exc_info=e
    #         )
    #
    # async def plain_hint(
    #         self,
    #         level: dto.Level,
    #         team: dto.Team,
    #         hint_number: int,
    #         run_at: datetime,
    # ):
    #     self.scheduler.add_job(
    #         func="shvatka.infrastructure.scheduler.wrappers:send_hint_wrapper",
    #         kwargs={
    #             "level_id": level.db_id,
    #             "team_id": team.id,
    #             "hint_number": hint_number
    #         },
    #         trigger="date",
    #         run_date=run_at,
    #         timezone=tz_utc,
    #     )
    #
    # async def plain_test_hint(
    #         self,
    #         suite: dto.LevelTestSuite,
    #         hint_number: int,
    #         run_at: datetime,
    # ):
    #     self.scheduler.add_job(
    #         func="shvatka.infrastructure.scheduler.wrappers:send_hint_for_testing_wrapper",
    #         kwargs={
    #             "level_id": suite.level.db_id,
    #             "game_id": suite.level.game_id,
    #             "player_id": suite.tester.player.id,
    #             "hint_number": hint_number,
    #         },
    #         trigger="date",
    #         run_date=run_at,
    #         timezone=tz_utc,
    #     )

    async def start(self):
        # TODO scheduler не стартует (выдается только в middleware data,
        #  нужно запускать самостоятельно)
        self.scheduler.start()

    async def close(self):
        self.scheduler.shutdown()
        self.executor.shutdown()
        self.job_store.shutdown()
