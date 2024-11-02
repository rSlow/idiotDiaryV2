import logging
import typing as t
from functools import wraps

import jwt
from dishka import FromDishka
from fastapi import HTTPException, Request
from starlette import status

from idiotDiary.core.db import dto
from idiotDiary.core.db.dao import DaoHolder
from idiotDiary.core.utils.auth.security import SecurityProps
from idiotDiary.core.utils.auth.token import Token
from idiotDiary.core.utils.exceptions.user import NoUsernameFound

logger = logging.getLogger(__name__)
T = t.TypeVar("T")
P = t.ParamSpec("P")


def auth_required(func: t.Callable[P, T]):
    @wraps(func)
    async def decorated(*args, user: FromDishka[dto.User], **kwargs):
        return await func(*args, user=user, **kwargs)

    return decorated


class AuthService:
    def __init__(self, security: SecurityProps) -> None:
        self.security = security

    async def authenticate_user(
            self, username: str, password: str,
            dao: DaoHolder
    ) -> dto.User:
        http_status_401 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            user = await dao.user.get_by_username_with_password(username)
        except NoUsernameFound as e:
            raise http_status_401 from e

        password_hash = user.hashed_password or ""
        if not self.security.verify_password(password, password_hash):
            raise http_status_401

        return user.without_password()

    async def update_user_password(
            self, user: dto.User, password: str, dao: DaoHolder
    ) -> None:
        hashed_password = self.security.get_password_hash(password)
        await dao.user.set_password(user, hashed_password)

    def create_user_token(self, user: dto.User) -> Token:
        return self.security.create_token(data={"sub": str(user.id_)})

    async def get_current_user(
            self, token: Token, dao: DaoHolder,
    ) -> dto.User:
        logger.debug("try to check token %s", token)
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload: dict = jwt.decode(
                token.value,
                key=self.security.secret_key,
                algorithms=[self.security.algorythm],
            )
            if payload.get("sub") is None:
                logger.warning("valid jwt contains no user id")
                raise credentials_exception
            user_db_id = int(t.cast(str, payload.get("sub")))

        except jwt.PyJWTError as e:
            logger.info("invalid jwt", exc_info=e)
            raise credentials_exception from e

        except Exception as e:
            logger.warning("some jwt error", exc_info=e)
            raise e

        try:
            user = await dao.user.get_by_id(user_db_id)
        except Exception as e:
            logger.info("user by id %s not found", user_db_id)
            raise credentials_exception from e

        return user

    async def get_user_basic(
            self, request: Request, dao: DaoHolder
    ) -> dto.User | None:
        if (header := request.headers.get("Authorization")) is None:
            return None

        schema, token = header.split(" ", maxsplit=1)
        if schema.lower() != "basic":
            return None
        username, password = self.security.decode_basic_auth(header)
        return await self.authenticate_user(username, password, dao)
