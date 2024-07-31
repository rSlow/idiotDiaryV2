from dishka import Provider, provide, Scope

from idiotDiary.core.config.models.main import Paths, BaseConfig
from idiotDiary.core.config.models.main import WebConfig
from idiotDiary.core.config.parser.paths import get_paths
from idiotDiary.core.data.storage.config.models import StorageConfig

from idiotDiary.tgbot.config.models.bot import BotConfig, TgClientConfig
from idiotDiary.tgbot.config.models.main import TgBotConfig
from idiotDiary.tgbot.config.parser.main import load_config as load_bot_config


class BaseConfigProvider(Provider):
    scope = Scope.APP

    def __init__(self, path_env: str = "SHVATKA_PATH"):
        super().__init__()
        self.path_env = path_env

    @provide
    def get_paths(self) -> Paths:
        return get_paths(self.path_env)

    # TODO посмотреть конфиги

    @provide
    def get_tgbot_config(self, paths: Paths) -> TgBotConfig:
        return load_bot_config(paths)

    @provide
    def get_base_config(self, config: TgBotConfig) -> BaseConfig:
        return config

    @provide
    def get_bot_config(self, config: TgBotConfig) -> BotConfig:
        return config.bot

    @provide
    def get_bot_storage_config(self, config: TgBotConfig) -> StorageConfig:
        return config.storage

    @provide
    def get_tg_client_config(self, config: TgBotConfig) -> TgClientConfig:
        return config.tg_client

    @provide
    def get_web_app_config(self, config: TgBotConfig) -> WebConfig:
        return config.web
