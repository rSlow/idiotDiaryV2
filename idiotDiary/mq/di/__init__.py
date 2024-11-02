__all__ = [
    "get_taskiq_providers"
]

from dishka import Provider

from .selenuim import SeleniumProvider
from .taskiq import TaskiqProvider


def get_taskiq_providers() -> list[Provider]:
    return [
        TaskiqProvider(),
        SeleniumProvider()
    ]
