from __future__ import annotations

from dataclasses import dataclass

from idiotDiary.core.config import BaseConfig
from .api import ApiConfig


@dataclass
class ApiAppConfig(BaseConfig):
    api: ApiConfig

    @classmethod
    def from_base(cls, base: BaseConfig, api: ApiConfig):
        return cls(
            paths=base.paths, db=base.db, redis=base.redis, app=base.app,
            web=base.web, mq=base.mq,
            api=api, auth=base.auth,
        )