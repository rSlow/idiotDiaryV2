from dishka import Provider, provide, Scope, from_context
from fastapi import HTTPException, Request
from jwt import PyJWTError

from idiotDiary.api.utils.auth import AuthService
from idiotDiary.api.utils.auth.cookie import OAuth2PasswordBearerWithCookie
from idiotDiary.core.data.db import dto
from idiotDiary.core.data.db.dao import DaoHolder


class AuthProvider(Provider):
    scope = Scope.APP

    request = from_context(provides=Request, scope=Scope.REQUEST)

    auth_service = provide(AuthService)

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
            return await auth_service.get_current_user(token, dao)
        except (PyJWTError, HTTPException):
            user = await auth_service.get_user_basic(request, dao)
            if user is None:
                raise
            return user
