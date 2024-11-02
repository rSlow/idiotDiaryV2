from __future__ import annotations

from dataclasses import dataclass, field

from adaptix import Retort
from aiogram import types as tg

user_retort = Retort()


@dataclass
class User:
    id_: int | None = None
    tg_id: int | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_bot: bool | None = None
    is_superuser: bool | None = None
    is_active: bool | None = None
    roles: list[UserRole] = field(default_factory=list)

    @property
    def fullname(self) -> str:
        if self.first_name is None:
            return ""
        if self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def name_mention(self) -> str:
        return (self.fullname
                or self.username
                or str(self.tg_id)
                or str(self.id_)
                or "unknown")

    @classmethod
    def from_aiogram(cls, user: tg.User) -> User:
        return cls(
            tg_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_bot=user.is_bot,
            is_active=True
        )

    def with_password(self, hashed_password: str) -> UserWithCreds:
        user_data = user_retort.dump(self, User)
        user_data["hashed_password"] = hashed_password
        return user_retort.load(user_data, UserWithCreds)


@dataclass
class UserWithCreds(User):
    hashed_password: str | None = None

    def without_password(self) -> User:
        user_data = user_retort.dump(self, UserWithCreds)
        return user_retort.load(user_data, User)


@dataclass
class UserRole:
    name: str
    alias: str
    id_: int | None = None

    @property
    def mention(self):
        return f"{self.alias} ({self.name})"
