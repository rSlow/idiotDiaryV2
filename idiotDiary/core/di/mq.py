import logging

from dishka import Provider, Scope, provide
from faststream.broker.core.abc import ABCBroker
from faststream.rabbit import RabbitBroker

from idiotDiary.core.config.models import BaseConfig, MQConfig

logger = logging.getLogger(__name__)


class MQProvider(Provider):
    scope = Scope.APP

    @provide
    def get_mq_config(self, base_config: BaseConfig) -> MQConfig:
        return base_config.mq

    @provide
    def get_broker(self, config: MQConfig) -> ABCBroker:
        logger.info(f"Broker configured with url: {config.uri}")
        return RabbitBroker(url=config.uri)
