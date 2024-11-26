from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka as setup_taskiq_dishka
from taskiq import TaskiqEvents

from idiotDiary.bot.config.models import BotAppConfig
from idiotDiary.bot.config.parser.main import load_config as load_bot_config
from idiotDiary.bot.di import get_bot_providers
from idiotDiary.core.config.parser.paths import get_paths
from idiotDiary.core.config.parser.retort import get_base_retort
from idiotDiary.core.di import get_common_providers
from idiotDiary.mq import middlewares
from idiotDiary.mq.broker import broker
from idiotDiary.mq.config.models.main import TaskiqAppConfig
from idiotDiary.mq.config.parser.main import load_config as load_taskiq_config
from idiotDiary.mq.di import get_taskiq_providers


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def worker_startup(*_):
    paths = get_paths()
    retort = get_base_retort()
    taskiq_config = load_taskiq_config(paths, retort)
    bot_config = load_bot_config(paths, retort)

    di_container = make_async_container(
        *get_common_providers(app_config=taskiq_config),
        *get_taskiq_providers(),
        *get_bot_providers(),
        context={
            TaskiqAppConfig: taskiq_config,
            BotAppConfig: bot_config
        }
    )
    setup_taskiq_dishka(di_container, broker)

    middlewares.setup(broker)


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def worker_shutdown(*_):
    pass
