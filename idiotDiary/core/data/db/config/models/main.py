from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DBConfig:
    echo: bool
    type: str | None = None
    connector: str | None = None
    host: str | None = None
    port: int | None = None
    login: str | None = None
    password: str | None = None
    name: str | None = None
    path: str | None = None
    echo: bool = False

    @property
    def uri(self):
        if self.type in ("mysql", "postgresql"):
            url = self.type
            if self.connector:
                url += self.connector
            url += f"://{self.login}:{self.password}@{self.host}:{self.port}/{self.name}"
        elif self.type == "sqlite":
            url = f"{self.type}://{self.path}"
        else:
            raise ValueError("DB_TYPE not mysql, sqlite or postgres")
        logger.debug(url)
        return url
