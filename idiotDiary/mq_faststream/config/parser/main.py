from adaptix import Retort

from goToVladi.core.config import Paths
from goToVladi.core.config.parser.config_file_reader import read_config_yaml
from goToVladi.core.config.parser.main import load_base_config
from goToVladi.mq.config.models.main import MQAppConfig


def load_config(paths: Paths, retort: Retort):
    config_dct = read_config_yaml(paths)

    return MQAppConfig.from_base(
        base=load_base_config(config_dct, paths, retort),
    )
