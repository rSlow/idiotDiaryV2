import logging

from dishka import Provider, provide
from jinja2 import Environment, FileSystemLoader, BaseLoader

from idiotDiary.bot.config.models.bot import BotConfig

logger = logging.getLogger(__name__)


class JinjaProvider(Provider):
    @provide
    def get_environment(self, loader: BaseLoader) -> Environment:
        env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True
        )
        logger.info("Jinja init:")  # TODO log init jinja, f.e. counting templates of s.e.
        return env

    @provide
    def get_loader(self, bot_config: BotConfig) -> BaseLoader:
        return FileSystemLoader(
            searchpath=bot_config.templates_dir  # TODO продумать папку с шаблонами
        )
