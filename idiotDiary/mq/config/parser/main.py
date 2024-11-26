from adaptix import Retort

from idiotDiary.core.config import Paths
from idiotDiary.core.config.parser.config_file_reader import read_config_yaml
from idiotDiary.core.config.parser.main import load_base_config
from idiotDiary.mq.config.models.backend import ResultBackendConfig
from idiotDiary.mq.config.models.main import TaskiqAppConfig
from idiotDiary.mq.config.models.selenium import SeleniumConfig


def load_config(paths: Paths, retort: Retort):
    config_dct = read_config_yaml(paths)

    return TaskiqAppConfig.from_base(
        base=load_base_config(config_dct, paths, retort),
        result_backend=retort.load(config_dct["mq"]["backend"], ResultBackendConfig),
        selenium=retort.load(config_dct["selenium"], SeleniumConfig),
    )
