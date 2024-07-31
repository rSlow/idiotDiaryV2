from dataclasses import dataclass


@dataclass
class RedisConfig:
    url: str
    port: int = 6379
    db: int = 1
