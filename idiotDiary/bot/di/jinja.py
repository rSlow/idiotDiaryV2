import logging

from dishka import Provider, provide, Scope
from jinja2 import Environment, FileSystemLoader, BaseLoader, Template

from idiotDiary.bot.views import jinja
from idiotDiary.core.config import Paths

logger = logging.getLogger(__name__)


class JinjaRenderer:
    def __init__(self, environment: Environment):
        self.environment = environment

    def render_template(
            self, template_name: str | Template, context: dict | None = None
    ):
        template = self.environment.get_template(template_name)
        return jinja.render_template(template, context)


class JinjaProvider(Provider):
    scope = Scope.APP

    renderer = provide(JinjaRenderer)

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
