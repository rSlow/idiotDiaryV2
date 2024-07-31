from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from aiogram.client.telegram import TelegramAPIServer


@dataclass
class BotApiConfig:
    type: BotApiType
    botapi_url: str | None = None
    botapi_file_url: str | None = None

    @property
    def is_local(self) -> bool:
        return self.type == BotApiType.local

    def create_server(self) -> TelegramAPIServer:
        if not self.is_local:
            raise RuntimeError("can create only local botapi server")
        return TelegramAPIServer(
            base=f"{self.botapi_url}/bot{{token}}/{{method}}",
            file=f"{self.botapi_file_url}{{path}}",
        )


class BotApiType(Enum):
    official = "official"
    # official = auto() # TODO проверить auto() enum
    local = "local"
