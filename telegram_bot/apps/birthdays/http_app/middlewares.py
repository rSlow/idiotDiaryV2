from typing import Callable

from aiohttp import web
from sqlalchemy.ext.asyncio import async_sessionmaker


@web.middleware
async def user_id_middleware(request: web.Request,
                             handler: Callable,
                             **kwargs):
    str_user_id = request.headers.get("X-Telegram-User-ID")
    if str_user_id is None:
        return web.Response(status=403)
    try:
        user_id = int(str_user_id)
    except ValueError:
        return web.Response(status=422)
    try:
        return await handler(request, user_id=user_id, **kwargs)
    except TypeError:
        return web.Response(status=404)


def session_middleware(session_pool: async_sessionmaker):
    @web.middleware
    async def inner_session_middleware(request: web.Request,
                                       handler: Callable,
                                       **kwargs):
        async with session_pool() as session:
            return await handler(request, session=session, **kwargs)

    return inner_session_middleware
