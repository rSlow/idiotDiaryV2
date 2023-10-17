from aiogram import types
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi import status
from starlette.routing import Match

from apps.not_working_place.http_app.routers import nwp_router
from config import settings
from config.logger import logger
from config.bot import dp, bot

app = FastAPI()

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


# @app.middleware("http")
async def log_middle(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    routes = request.app.router.routes
    logger.debug("Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
            for name, value in scope["path_params"].items():
                logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")

    response = await call_next(request)
    return response
