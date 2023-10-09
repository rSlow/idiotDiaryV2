from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .settings import ENV


class Base(DeclarativeBase):
    pass


URL = ENV.str("DATABASE_URL")

Engine = create_async_engine(
    url=URL,
    echo=True,
)
Session = async_sessionmaker(
    bind=Engine,
    expire_on_commit=False,
    autoflush=True
)


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


async def create_database() -> None:
    try:
        from ORM.models.user import User
        from ORM.models.room import GameRoom
        from ORM.models.player import GamePlayer
        from ORM.models.piece import GamePiece

    except ImportError:
        raise


async def stop_database() -> None:
    await Engine.dispose()
