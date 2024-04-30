from aiogram.webhook.aiohttp_server import setup_application as setup
from aiohttp.web import run_app

from config import settings
from config.bot import dp, bot, init_dispatcher
from http_server.app import app as http_app

if __name__ == '__main__':
    init_dispatcher(dp)
    setup(http_app, dp, bot=bot)
    run_app(
        http_app,
        host="0.0.0.0",
        port=settings.WEB_SERVER_PORT,
    )
