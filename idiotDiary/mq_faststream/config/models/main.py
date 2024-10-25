from dataclasses import dataclass

from idiotDiary.core.config import BaseConfig


@dataclass
class MQAppConfig(BaseConfig):
    @classmethod
    def from_base(cls, base: BaseConfig):
        return MQAppConfig(
            app=base.app, paths=base.paths, db=base.db, redis=base.redis,
            web=base.web, mq=base.mq, auth=base.auth
        )
