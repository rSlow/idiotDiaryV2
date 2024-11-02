from dataclasses import dataclass

from idiotDiary.core.config.models import RedisConfig


@dataclass
class ResultBackendConfig(RedisConfig):
    pass
