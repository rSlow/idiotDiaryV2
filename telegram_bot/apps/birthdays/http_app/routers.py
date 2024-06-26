from json import JSONDecodeError

from aiohttp import web
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from common.ORM.database import Session
from config.logger import logger
from .middlewares import user_id_middleware, session_middleware
from .schemas import SBirthday, uuid_validator, UUIDValidationError
from ..ORM.birthdays import Birthday

birthdays_router = web.RouteTableDef()


@birthdays_router.put("/")
async def update_birthday(request: web.Request,
                          user_id: int,
                          session: AsyncSession):
    try:
        raw_data = await request.json()
        data = [SBirthday(**birthday_data) for birthday_data in raw_data]
        await Birthday.update_data(
            data=data,
            user_id=user_id,
            session=session
        )
        return web.Response()
    except (ValidationError, JSONDecodeError):
        logger.exception("Error with decoding data!")
        return web.Response(status=422)
    except IntegrityError:
        logger.exception("Already existed UUID!")
        return web.Response(status=409)


@birthdays_router.delete("/")
async def delete_birthdays(_: web.Request,
                           user_id: int,
                           session: AsyncSession):
    await Birthday.delete_data(
        user_id=user_id,
        session=session
    )
    return web.Response()


@birthdays_router.delete("/{uuid}/")
async def delete_birthday(request: web.Request,
                          user_id: int,
                          session: AsyncSession):
    uuid_str = request.match_info.get("uuid")
    try:
        uuid = uuid_validator(uuid_str)
        deleted = await Birthday.delete_birthday(
            uuid=uuid,
            user_id=user_id,
            session=session
        )
        if not deleted:
            return web.Response(status=404)
        return web.Response()
    except UUIDValidationError:
        return web.Response(status=422)


birthdays_app = web.Application(middlewares=[
    user_id_middleware,
    session_middleware(session_pool=Session)
])
birthdays_app.add_routes(birthdays_router)
