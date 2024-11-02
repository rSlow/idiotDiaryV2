from dataclasses import dataclass

from .redis import RedisConfig


@dataclass
class ResultBackendConfig(RedisConfig):
    pass


@dataclass
class MQConfig:
    host: str
    port: int
    user: str
    password: str
    backend: ResultBackendConfig | None = None

    @property
    def uri(self):
        url = f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"
        return url
