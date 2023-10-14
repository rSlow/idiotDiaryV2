from uvicorn import run as fastapi_run

from config.bot import dp, bot
from config.settings import WEB_SERVER_HOST, WEB_SERVER_PORT
from http_server.app import app as fastapi_app
from http_server.webhook import fastapi_setup

if __name__ == '__main__':
    fastapi_setup(fastapi_app, dp, bot=bot)
    fastapi_run(fastapi_app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
