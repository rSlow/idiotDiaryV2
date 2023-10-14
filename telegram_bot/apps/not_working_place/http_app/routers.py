from fastapi import APIRouter, Body

from .schemas import SBirthday
from ..ORM.birthdays import Birthday

nwp_router = APIRouter(prefix="/nwp")


@nwp_router.post("/update_birthday", response_model=None)
async def update_birthday(data: list[SBirthday] = Body()):
    await Birthday.update_data(data)
    return {"detail": "ok"}
