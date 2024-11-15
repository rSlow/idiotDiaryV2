import logging
from functools import partial

import uvicorn
from aiogram import Bot, Dispatcher
from dishka import make_async_container, AsyncContainer
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka

from idiotDiary.api import create_app as create_api_app, ApiAppConfig
from idiotDiary.api.config.models import ApiConfig
from idiotDiary.api.config.parser.main import load_config as load_api_config
from idiotDiary.api.di import get_api_providers
from idiotDiary.api.utils.webhook.handler import SimpleRequestHandler
from idiotDiary.api.utils.webhook.setup import setup_lifespan
from idiotDiary.bot.config.models import BotAppConfig
from idiotDiary.bot.config.models.webhook import WebhookConfig
from idiotDiary.bot.config.parser.main import load_config as load_bot_config
from idiotDiary.bot.di import get_bot_providers
from idiotDiary.bot.di.dp import resolve_update_types
from idiotDiary.bot.utils import ui
from idiotDiary.core.config.models import WebConfig
from idiotDiary.core.config.parser.config_logging import setup_logging
from idiotDiary.core.config.parser.paths import get_paths
from idiotDiary.core.config.parser.retort import get_base_retort
from idiotDiary.core.di import get_common_providers
from idiotDiary.core.scheduler.scheduler import ApScheduler
from idiotDiary.core.utils import di_visual
from idiotDiary.mq.broker import broker

logger = logging.getLogger(__name__)


def main():
    paths = get_paths()
    setup_logging(paths)

    retort = get_base_retort()
    api_config = load_api_config(paths, retort)
    bot_config = load_bot_config(paths, retort)
    webhook_config = bot_config.bot.webhook

    di_container = make_async_container(
        *get_common_providers(bot_config),
        *get_bot_providers(),
        *get_api_providers(),
        context={
            ApiAppConfig: api_config,
            BotAppConfig: bot_config,
        }
    )

    api_app = create_api_app(api_config)
    setup_lifespan(api_app, di_container)

    webhook_handler = SimpleRequestHandler(secret_token=webhook_config.secret)
    webhook_handler.register(api_app, webhook_config.path)

    setup_fastapi_dishka(di_container, api_app)

    startup_callback = partial(
        on_startup,
        di_container, api_config.web, api_config.api, webhook_config
    )
    shutdown_callback = partial(on_shutdown, di_container)
    api_app.add_event_handler("startup", startup_callback)
    api_app.add_event_handler("shutdown", shutdown_callback)

    logger.info(
        "app prepared with dishka:\n%s",
        di_visual.render(
            [di_container.registry, *di_container.child_registries],
        ),
    )
    return api_app


async def on_startup(
        dishka: AsyncContainer,
        web_config: WebConfig, api_config: ApiConfig,
        webhook_config: WebhookConfig
):
    webhook_url = (
            web_config.real_base_url +  # domain + proxy
            api_config.root_path + webhook_config.path
    )

    bot = await dishka.get(Bot)
    dp: Dispatcher = await dishka.get(Dispatcher)
    await bot.set_webhook(
        url=webhook_url,
        secret_token=webhook_config.secret,
        allowed_updates=resolve_update_types(dp),
    )
    logger.info("as webhook url used %s", webhook_url)

    await ui.setup(bot)
    await broker.startup()

    await dishka.get(ApScheduler)  # run scheduler


async def on_shutdown(dishka: AsyncContainer):
    bot: Bot = await dishka.get(Bot)
    await bot.delete_webhook()
    logger.info("webhook deleted")

    await dishka.close()


def run():
    uvicorn.run(
        app="idiotDiary.__main__:main",
        host="0.0.0.0",
        port=8000,
        factory=True
    )


if __name__ == '__main__':
    run()
