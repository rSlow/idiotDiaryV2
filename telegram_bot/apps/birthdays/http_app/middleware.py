from typing import Callable

from aiohttp import web


@web.middleware
async def user_id_middleware(request: web.Request,
                             handler: Callable):
    str_user_id = request.headers.get("user_id")
    if str_user_id is None:
        return web.Response(status=403)
    try:
        user_id = int(str_user_id)
    except ValueError:
        return web.Response(status=422)

    return await handler(request, user_id=user_id)
