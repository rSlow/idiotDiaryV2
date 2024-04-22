from typing import Annotated

from aiogram import types
from fastapi import FastAPI, Header, HTTPException, status, Body, Request
from starlette.responses import JSONResponse

from apps.birthdays.http_app.routers import birthdays_router
from config import settings
from loguru import logger
from config.bot import dp, bot
from http_server.setup import fastapi_setup

app = FastAPI(
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url=None
)

app.include_router(birthdays_router)


@app.post(settings.WEBHOOK_PATH, include_in_schema=False)
async def bot_webhook(update: Annotated[dict, Body()],
                      secret_token: Annotated[str, Header(alias="X-Telegram-Bot-Api-Secret-Token")]):
    if secret_token != settings.WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect secret token",
        )

    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


@app.exception_handler(HTTPException)
async def exception_logger(_: Request,
                           exc: HTTPException):
    logger.error(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
        *exc.args
    )


fastapi_setup(app, dp, bot)
