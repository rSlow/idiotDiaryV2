import importlib
from pathlib import Path
from typing import cast

from idiotDiary.bot.forms.shaurma.utils.types import RenderFunc
from idiotDiary.mq.broker import broker


@broker.task
def draw_screenshot(module_func: str, temp_dir: Path, **data) -> Path:
    module_str, func_str = module_func.rsplit(":", maxsplit=1)
    module = importlib.import_module(module_str)
    func = cast(RenderFunc, getattr(module, func_str))
    return func(temp_dir=temp_dir, **data)
