from dataclasses import dataclass


@dataclass
class MQConfig:
    host: str
    port: int
    user: str
    password: str

    @property
    def uri(self):
        url = f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"
        return url
