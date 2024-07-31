from adaptix import Retort

from idiotDiaryV3.common.config.models.paths import Paths
from idiotDiaryV3.common.config.parser.config_file_reader import read_config_yaml
from idiotDiaryV3.common.config.parser.main import load_base_config
from idiotDiaryV3.common.data.parser.storage import load_storage_config
from idiotDiaryV3.tgbot.config.models.bot import TgClientConfig, BotConfig
from idiotDiaryV3.tgbot.config.models.main import TgBotConfig


def load_config(paths: Paths,
                retort: Retort) -> TgBotConfig:
    config_dct = read_config_yaml(paths)
    bot_config = retort.load(config_dct["bot"], BotConfig)
    return TgBotConfig.from_base(
        base=load_base_config(config_dct, paths, retort),
        bot=bot_config,
        storage=load_storage_config(config_dct["storage"], retort),
        tg_client=TgClientConfig(bot_token=bot_config.token),
    )
