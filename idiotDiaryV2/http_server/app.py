from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web

from apps.birthdays.http_app.routers import birthdays_app
from config import settings
from config.bot import dp, bot

app = web.Application()

webhook_requests_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
    secret_token=settings.WEBHOOK_SECRET,
)
webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)

app.add_subapp("/birthdays", birthdays_app)
