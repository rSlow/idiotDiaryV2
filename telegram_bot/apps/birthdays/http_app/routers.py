from json import JSONDecodeError
from typing import Annotated
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from fastapi import Response, APIRouter, HTTPException
from starlette import status

from http_server.dependencies import DependsAsyncSession
from .dependencies import DependsUserID

from fastapi import Body

from .schemas import SBirthday
from ..ORM.birthdays import Birthday

birthdays_router = APIRouter(prefix="/birthdays")


@birthdays_router.put("/", response_model=None)
async def update_birthday(data: Annotated[list[SBirthday], Body()],
                          user_id: DependsUserID,
                          session: DependsAsyncSession):
    try:
        await Birthday.update_data(
            data=data,
            user_id=user_id,
            session=session
        )
        return Response()
    except (ValidationError, JSONDecodeError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Error with decoding data!"
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already existed UUID!"
        )


@birthdays_router.delete("/")
async def delete_birthdays(user_id: DependsUserID,
                           session: DependsAsyncSession):
    await Birthday.delete_data(
        user_id=user_id,
        session=session
    )
    return Response()


@birthdays_router.delete("/{uuid}")
async def delete_birthday(uuid: UUID,
                          user_id: DependsUserID,
                          session: DependsAsyncSession):
    deleted = await Birthday.delete_birthday(
        uuid=uuid,
        user_id=user_id,
        session=session
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"UUID {uuid} wasn't deleted"
        )
    return Response(content="ok")
