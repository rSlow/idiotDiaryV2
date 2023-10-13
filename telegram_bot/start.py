from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web

from config.bot import dp, bot
from config.settings import WEB_SERVER_HOST, WEB_SERVER_PORT
from http_server.app import app

if __name__ == '__main__':
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
