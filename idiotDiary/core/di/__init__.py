from idiotDiary.bot.di.bot import BotProvider
from idiotDiary.core.di.config import BaseConfigProvider, DbConfigProvider
from idiotDiary.core.di.db import DbProvider
from idiotDiary.core.di.redis import RedisProvider
from idiotDiary.core.di.retort import RetortProvider


def get_providers(paths_env):
    return [
        BaseConfigProvider(paths_env),
        RetortProvider(),
        DbConfigProvider(),
        DbProvider(),
        RedisProvider(),
        FileClientProvider(),
        BotProvider(),
    ]
