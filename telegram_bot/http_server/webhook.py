import logging

from aiogram import Bot

from config import settings


async def init_webhook(bot: Bot):
    webhook_url = f"{settings.BASE_WEBHOOK_URL}:{settings.BASE_WEBHOOK_PORT}{settings.WEBHOOK_PATH}"
    await bot.set_webhook(
        url=webhook_url,
        secret_token=settings.WEBHOOK_SECRET
    )
    logging.info("SET WEBHOOK")
