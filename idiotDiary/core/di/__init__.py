from .config import BaseConfigProvider
from .dao import DaoProvider
from .db import DbProvider
from .lock import LockProvider
from .redis import RedisProvider
from .scheduler import SchedulerProvider
from .security import SecurityProvider


def get_common_sync_providers():
    return [
        BaseConfigProvider(),
        SecurityProvider(),
    ]


def get_common_providers():
    return [
        *get_common_sync_providers(),
        DbProvider(),
        DaoProvider(),
        RedisProvider(),
        LockProvider(),
        SchedulerProvider(),
    ]
