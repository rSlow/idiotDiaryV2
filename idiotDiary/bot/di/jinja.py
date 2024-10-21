import logging

from dishka import Provider, provide, Scope
from jinja2 import Environment, FileSystemLoader, BaseLoader

from idiotDiary.core.config import Paths

logger = logging.getLogger(__name__)


class JinjaProvider(Provider):
    scope = Scope.APP

    @provide
    def get_environment(self, loader: BaseLoader) -> Environment:
        env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True
        )
        logger.info(f"Jinja init with loader <{loader.__class__.__name__}>")
        return env

    @provide
    def get_loader(self, paths: Paths) -> BaseLoader:
        return FileSystemLoader(
            searchpath=paths.bot_path / "views" / "jinja" / "templates"
        )
