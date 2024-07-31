import logging
from functools import partial

import uvicorn
from aiogram import Bot, Dispatcher
from dishka import make_async_container, AsyncContainer
from fastapi import FastAPI

from idiotDiary.common.config.parser.config_logging import setup_logging
from idiotDiary.common.config.parser.paths import get_paths
from idiotDiary.api.main import create_app as create_api_app
from idiotDiary.api.config.parser.main import load_config as load_api_config
from idiotDiary.bot.config.parser.main import load_config as load_bot_config
from idiotDiary.common.config.parser.retort import get_base_retort

logger = logging.getLogger(__name__)


def main():
    paths = get_paths()
    base_retort = get_base_retort()

    setup_logging(paths)

    api_config = load_api_config(paths, base_retort)
    bot_config = load_bot_config(paths, base_retort)
    webhook_config = bot_config.bot.webhook

    api_app = create_api_app(api_config)

    di_container = make_async_container(
        *get_providers("SHVATKA_PATH"),
        *get_bot_specific_providers(),
        *get_api_specific_providers(),
    )

    root_app = FastAPI()
    setup = partial(on_startup, di_container, webhook_config)
    root_app.add_event_handler("startup", setup)
    logger.info(
        "app prepared with dishka:\n%s",
        render([di_container.registry, *di_container.child_registries], di_container),
    )
    return root_app


async def on_startup(dishka: AsyncContainer,
                     webhook_config: WebhookConfig):
    webhook_url = webhook_config.web_url + webhook_config.path
    logger.info("as webhook url used %s", webhook_url)
    bot = await dishka.get(Bot)
    dp = await dishka.get(Dispatcher)
    await bot.set_webhook(
        url=webhook_url,
        secret_token=webhook_config.secret,
        # allowed_updates=resolve_update_types(dp),
    )


def run():
    uvicorn.run(
        app=main,
        host="0.0.0.0",
        port=8000
    )


if __name__ == '__main__':
    run()
