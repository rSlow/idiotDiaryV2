from typing import Optional

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from jinja2 import Environment

from idiotDiary.bot.views.jinja import render_template


class JinjaTemplate(Text):
    def __init__(
            self, env: Environment, template_name: str,
            template_data: Optional[dict] = None, when: WhenCondition = None
    ):
        super().__init__(when=when)
        self._env = env
        self._template_name = template_name
        if template_data is None:
            self._template_data = {}
        else:
            self._template_data = template_data.copy()

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        self._template_data.update(data)
        template = self._env.get_template(self._template_name)
        return render_template(
            template=template,
            context=self._template_data,
        )
