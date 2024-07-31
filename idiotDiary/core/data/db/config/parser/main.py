from adaptix import Retort

from ..models.main import DBConfig


def load_db_config(db_dict: dict,
                   retort: Retort) -> DBConfig:
    return retort.load(db_dict, DBConfig)
