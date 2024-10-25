from dataclasses import dataclass


@dataclass
class SeleniumConfig:
    host: str
    port: int
    login: str
    password: str

    @property
    def uri(self):
        return f""
