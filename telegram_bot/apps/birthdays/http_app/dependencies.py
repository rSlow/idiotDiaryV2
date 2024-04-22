from typing import Annotated

from fastapi import Header, HTTPException, Depends
from starlette import status


async def user_id_middleware(user_id: Annotated[str, Header(alias="X-Telegram-User-ID")]):
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No Telegram user ID is passed"
        )
    try:
        return int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unprocessable Telegram user ID"
        )


DependsUserID = Annotated[int, Depends(user_id_middleware)]
