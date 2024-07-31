import logging

from redis.asyncio import Redis
from idiotDiary.core.data.models.redis import RedisConfig

logger = logging.getLogger(__name__)


def create_redis(config: RedisConfig) -> Redis:
    logger.info("created redis for %s", config)
    return Redis(host=config.url, port=config.port, db=config.db)
