from aiogram.webhook.aiohttp_server import setup_application as setup
from aiogram_dialog import setup_dialogs
from aiohttp.web import run_app

from apps.free_shaurma.handlers import test_fsh_router
from common.handlers.errors import error_router
from common.handlers.main import start_router, main_menu
from config import settings
from config.logger import logger
from config.bot import dp, bot
from config.router import apps_router
from config.settings import WEB_SERVER_PORT
from config.startup_shutdown import on_startup, on_shutdown
from http_server.app import app as http_app

if __name__ == '__main__':
    setup(http_app, dp, bot=bot)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    setup_dialogs(dp)

    if settings.DEBUG:
        logger.warning("SET DEBUG MODE")

        dp.include_routers(
            test_fsh_router,
        )

    dp.include_routers(
        start_router,
        error_router,
        main_menu,
        apps_router,
    )

    run_app(
        http_app,
        host='0.0.0.0',
        port=WEB_SERVER_PORT,
    )
