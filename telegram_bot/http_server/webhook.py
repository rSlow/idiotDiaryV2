from aiogram import Dispatcher, Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from config import settings
from http_server.app import app


async def init_webhook(dp: Dispatcher, bot: Bot):
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)
    await bot.set_webhook(
        url=f"{settings.BASE_WEBHOOK_URL}{settings.WEBHOOK_PATH}",
        secret_token=settings.WEBHOOK_SECRET
    )
