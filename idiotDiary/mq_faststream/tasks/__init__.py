from faststream.broker.core.abc import ABCBroker

from . import mailing, logging


def setup(broker: ABCBroker):
    broker.include_router(mailing.router)
    broker.include_router(logging.router)
