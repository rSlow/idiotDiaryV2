from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ...data.models.db import DBConfig
from ...data.models.redis import RedisConfig
from .paths import Paths


@dataclass
class BaseConfig(Protocol):
    app: AppConfig
    paths: Paths
    db: DBConfig
    redis: RedisConfig
    web: WebConfig

    @property
    def app_dir(self) -> Path:
        return self.paths.app_dir

    @property
    def config_path(self) -> Path:
        return self.paths.config_path

    @property
    def log_path(self) -> Path:
        return self.paths.log_path


@dataclass
class AppConfig:
    name: str


@dataclass
class WebConfig:
    base_url: str
