import binascii

from dishka import Provider, provide, Scope, from_context
from fastapi import HTTPException, Request, status
from jwt import PyJWTError

from idiotDiary.api.utils.auth import AuthService
from idiotDiary.api.utils.auth.cookie import OAuth2PasswordBearerWithCookie
from idiotDiary.api.utils.exceptions import AuthError
from idiotDiary.core.db import dto
from idiotDiary.core.db.dao import DaoHolder


class AuthProvider(Provider):
    scope = Scope.APP

    auth_service = provide(AuthService)

    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide
    def get_cookie_auth(self) -> OAuth2PasswordBearerWithCookie:
        return OAuth2PasswordBearerWithCookie(token_url="auth/token")

    @provide(scope=Scope.REQUEST)
    async def get_current_user(
            self,
            request: Request,
            cookie_auth: OAuth2PasswordBearerWithCookie,
            auth_service: AuthService,
            dao: DaoHolder,
    ) -> dto.User:
        try:
            token = await cookie_auth.get_token(request)
            return await auth_service.get_user_from_bearer(token, dao)
        except (PyJWTError, AuthError):
            try:
                return await auth_service.get_user_from_basic(request, dao)
            except (binascii.Error, AuthError, ValueError):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
