from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum

from idiotDiary.core.data.redis.config.models import RedisConfig

logger = logging.getLogger(__name__)


class StorageType(Enum):
    memory = "memory"
    redis = "redis"


@dataclass
class StorageConfig:
    type_: StorageType
    redis: RedisConfig | None = None
