import asyncio

from dishka import make_async_container
from dishka.integrations.faststream import (
    setup_dishka as setup_dishka_faststream,
    FastStreamProvider
)
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from idiotDiary.bot.config.models import BotAppConfig
from idiotDiary.bot.config.parser.main import load_config
from idiotDiary.bot.di import get_bot_providers
from idiotDiary.core.config import setup_logging, BaseConfig
from idiotDiary.core.config.parser.paths import get_paths
from idiotDiary.core.config.parser.retort import get_base_retort
from idiotDiary.core.di import get_common_providers
from idiotDiary.mq import tasks
from idiotDiary.mq.config.models.main import MQAppConfig
from idiotDiary.mq.config.parser.main import load_config as load_mq_config
from idiotDiary.mq.di.context import FastStreamInjectContext
from idiotDiary.mq.utils import middlewares


def main():
    paths = get_paths()
    setup_logging(paths)

    retort = get_base_retort()
    mq_config = load_mq_config(paths, retort)
    bot_config = load_config(paths, retort)

    rabbit_broker = RabbitBroker(
        url=mq_config.mq.uri,
        max_consumers=30
    )
    mq_app = FastStream(rabbit_broker)

    di_container = make_async_container(
        *get_common_providers(),
        *get_bot_providers(),
        FastStreamProvider(),
        context={
            BaseConfig: mq_config.as_base(),
            MQAppConfig: mq_config,
            BotAppConfig: bot_config
        }
    )
    setup_dishka_faststream(di_container, mq_app)
    FastStreamInjectContext.container = di_container  # for exception handlers

    tasks.setup(rabbit_broker)
    middlewares.setup(rabbit_broker)
    rabbit_broker.publish()
    return mq_app


async def run():
    mq_app = main()
    await mq_app.run()


if __name__ == '__main__':
    asyncio.run(run())
