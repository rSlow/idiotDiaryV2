from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped, Session

from .database import Base, Engine


class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(unique=True)
    value: Mapped[str]

    @classmethod
    def get(cls,
            session: AsyncSession,
            key: str):
        q = select(cls).where(
            cls.key == key
        )
        with Session(Engine) as session:
            value = session.execute(q)
            return value

    @classmethod
    def get_all(cls,
                session: AsyncSession):
        ...

    @classmethod
    def set_value(cls,
                  session: AsyncSession,
                  key: str,
                  value: str):
        ...
