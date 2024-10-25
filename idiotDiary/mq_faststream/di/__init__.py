__all__ = [
    "get_mq_providers",
]

from dishka import Provider

from .selenuim import SeleniumProvider


def get_mq_providers() -> list[Provider]:
    return [
        SeleniumProvider(),
    ]
