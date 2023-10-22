from aiogram.webhook.aiohttp_server import setup_application as setup
from aiohttp.web import run_app

from config.bot import dp, bot
from config.settings import WEB_SERVER_HOST, WEB_SERVER_PORT
from http_server.app import app as http_app

if __name__ == '__main__':
    setup(http_app, dp, bot=bot)
    run_app(
        http_app,
        host=WEB_SERVER_HOST,
        port=WEB_SERVER_PORT,
    )
