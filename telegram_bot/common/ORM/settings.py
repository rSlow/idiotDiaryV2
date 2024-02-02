from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped, Session

from .database import Base, Engine


class Setting(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(nullable=True)

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
