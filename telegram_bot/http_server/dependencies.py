from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.ORM.database import Session


async def get_session():
    async with Session() as session:
        yield session


DependsAsyncSession = Annotated[AsyncSession, Depends(get_session)]
