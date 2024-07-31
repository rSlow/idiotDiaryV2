from adaptix import Retort

from idiotDiary.api.config.models.main import ApiConfig
from idiotDiary.api.config.parser.auth import load_auth
from idiotDiary.common.config.models.paths import Paths
from idiotDiary.common.config.parser.config_file_reader import read_config_yaml
from idiotDiary.common.config.parser.main import load_base_config


def load_config(paths: Paths,
                retort: Retort) -> ApiConfig:
    config_dct = read_config_yaml(paths)
    return ApiConfig.from_base(
        base=load_base_config(config_dct, paths, retort),
        auth=load_auth(config_dct["api"]["auth"]),
        context_path=config_dct["api"].get("context-path", ""),
        enable_logging=bool(config_dct["api"].get("enable-logging", False)),
    )
