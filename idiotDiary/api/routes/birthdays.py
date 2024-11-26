import logging
from typing import Annotated
from uuid import UUID

from aiohttp import web
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body, Path, Response
from sqlalchemy.exc import IntegrityError

from idiotDiary.api.utils.auth.service import auth_required
from idiotDiary.core.db import dto
from idiotDiary.core.db.dao import DaoHolder

logger = logging.getLogger(__name__)


@inject
async def update_birthdays(
        birthdays: Annotated[list[dto.Birthday], Body(default_factory=list)],
        user: FromDishka[dto.User], dao: FromDishka[DaoHolder]
):
    try:
        await dao.birthdays.update(birthdays, user.id_)
        return {"detail": "ok"}
    except IntegrityError:  # TODO
        logger.exception("Already existed UUID!")
        return web.Response(status=409)


@inject
async def delete_birthdays(
        user: FromDishka[dto.User], dao: FromDishka[DaoHolder]
):
    await dao.birthdays.delete_all_from_user(user.id_)
    return {"detail": "ok"}


@auth_required
@inject
async def delete_birthday(
        birthday_uuid: Annotated[UUID, Path()], dao: FromDishka[DaoHolder],
):
    deleted = await dao.birthdays.delete(birthday_uuid)
    if not deleted:
        return Response(status_code=404)
    return {"detail": "ok"}


def setup():
    router = APIRouter(prefix="/birthdays")

    router.add_api_route("/", update_birthdays, methods=["PUT"])
    router.add_api_route("/", delete_birthdays, methods=["DELETE"])
    router.add_api_route("/{birthday_uuid}/", delete_birthday, methods=["DELETE"])

    return router
