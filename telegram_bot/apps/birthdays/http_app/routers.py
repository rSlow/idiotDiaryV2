from aiohttp import web
from pydantic import ValidationError

from .schemas import SBirthday, uuid_validator, UUIDValidationError
from ..ORM.birthdays import Birthday

birthdays_router = web.RouteTableDef()


@birthdays_router.put("/birthdays")
async def update_birthday(request: web.BaseRequest):
    try:
        raw_data = await request.json()
        data = [SBirthday(**birthday_data) for birthday_data in raw_data]
        await Birthday.update_data(data)
        return web.Response()
    except ValidationError:
        return web.Response(status=422)


async def delete_birthdays(_: web.Request):
    await Birthday.delete_data()
    return web.Response()


@birthdays_router.delete("/birthdays/{uuid}")
async def delete_birthday(request: web.Request):
    uuid_str = request.match_info.get("uuid")
    try:
        uuid = uuid_validator(uuid_str)
        deleted = await Birthday.delete_birthday(uuid)
        if not deleted:
            return web.Response(status=404)
        return web.Response()
    except UUIDValidationError:
        return web.Response(status=422)


birthdays_app = web.Application()
birthdays_app.add_routes(birthdays_router)
