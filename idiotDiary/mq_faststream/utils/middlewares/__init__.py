__all__ = [
    ""
]

from faststream import BaseMiddleware
from faststream.broker.core.abc import ABCBroker

from goToVladi.mq.handlers.exceptions import exc_middleware


def setup(broker: ABCBroker):
    middlewares: list[type:BaseMiddleware] = [
        exc_middleware,
    ]
    for middleware in middlewares:
        broker.add_middleware(middleware)
