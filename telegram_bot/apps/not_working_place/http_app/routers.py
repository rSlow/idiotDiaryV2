from aiohttp import web

from .schemas import SBirthday
from ..ORM.birthdays import Birthday

nwp_router = web.RouteTableDef()
nwp_app = web.Application()


@nwp_router.put("/birthdays")
async def update_birthday(request: web.BaseRequest):
    raw_data = await request.json()
    data = [SBirthday(**birthday_data) for birthday_data in raw_data]
    await Birthday.update_data(data)
    return web.Response()


@nwp_router.delete("/birthdays")
async def update_birthday(_: web.BaseRequest):
    await Birthday.delete_data()
    return web.Response()


nwp_app.add_routes(nwp_router)
