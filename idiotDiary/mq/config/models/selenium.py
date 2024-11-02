from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class SeleniumDriverType(StrEnum):
    REMOTE = "remote"
    CHROME = "chrome"


@dataclass
class SeleniumConfig:
    type_: SeleniumDriverType
    host: str | None = None
    port: int | None = None
    path: Path | str | None = None

    @property
    def uri(self):
        res = "http://" + self.host
        if self.port is not None:
            res += f":{self.port}"
        return res + "/wd/hub"
