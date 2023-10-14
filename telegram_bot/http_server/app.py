from aiogram import types
from fastapi import FastAPI, HTTPException, Header
from fastapi import status

from apps.not_working_place.http_app.routers import nwp_router
from config import settings
from config.bot import dp, bot
from http_server.webhook import webhook_router

app = FastAPI()

app.include_router(webhook_router)
app.include_router(nwp_router)


@app.post(settings.WEBHOOK_PATH)
async def bot_webhook(update: dict,
                      secret_token: str = Header(alias=settings.SECRET_HEADER)):
    if secret_token != settings.WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect secret token",
        )

    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)
