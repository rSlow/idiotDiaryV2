from dishka import Provider, Scope, provide

from idiotDiary.core.utils.auth.security import SecurityProps


class SecurityProvider(Provider):
    scope = Scope.APP

    security = provide(SecurityProps)
