from fastapi import APIRouter, Body

from .schemas import SBirthday
from ..ORM.birthdays import Birthday

nwp_router = APIRouter(prefix="/nwp")


@nwp_router.put("/birthdays", response_model=None)
async def update_birthday(data: list[SBirthday] = Body()):
    await Birthday.update_data(data)


@nwp_router.delete("/birthdays")
async def update_birthday():
    await Birthday.delete_data()
