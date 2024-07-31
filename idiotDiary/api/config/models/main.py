from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol, Self

from shvatka.api.config.models.auth import AuthConfig
from idiotDiary.common.config.models.main import BaseConfig


@dataclass
class ApiConfig(BaseConfig):
    auth: AuthConfig
    context_path: str = ""
    enable_logging: bool = False

    @classmethod
    def from_base(
            cls,
            base: BaseConfig,
            auth: AuthConfig,
            context_path: str = "",
            enable_logging: bool = False,
    ):
        return cls(
            paths=base.paths,
            db=base.db,
            redis=base.redis,
            auth=auth,
            context_path=context_path,
            app=base.app,
            enable_logging=enable_logging,
            web=base.web,
        )
