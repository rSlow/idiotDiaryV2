from typing import Any

from adaptix import Retort

from ..models.main import StorageConfig, StorageType
from .redis import load_redis_config


def load_storage_config(dct: dict[str, Any],
                        retort: Retort) -> StorageConfig:
    config = StorageConfig(type_=StorageType[dct["type"]])
    if config.type_ == StorageType.redis:
        config.redis = load_redis_config(dct["redis"], retort)
    return config
