from adaptix import Retort
from dishka import Provider, Scope, provide

from idiotDiary.api.config.models.main import ApiConfig
from idiotDiary.api.config.parser.main import load_config
from idiotDiary.common.config import Paths


class ApiConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_api_config(self,
                       paths: Paths,
                       base_retort: Retort) -> ApiConfig:
        return load_config(paths, base_retort)

    @provide
    def get_auth_config(self, config: ApiConfig) -> AuthConfig:
        return config.auth
