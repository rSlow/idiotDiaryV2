from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp.web_app import Application

from apps.not_working_place.http_app.routers import nwp_app
from config import settings
from config.bot import dp, bot

app = Application()

webhook_requests_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
    secret_token=settings.WEBHOOK_SECRET,
)
webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)

app.add_subapp("/nwp", nwp_app)
