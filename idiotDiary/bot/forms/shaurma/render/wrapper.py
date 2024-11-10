from pathlib import Path
from typing import cast

import aiofiles.tempfile as atf
from aiogram import types
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from taskiq import AsyncTaskiqTask, TaskiqResult

from idiotDiary.bot.forms.shaurma.utils.types import RenderFunc
from idiotDiary.bot.states.start import MainMenuSG
from idiotDiary.bot.utils.dialog_factory import OnFinish
from idiotDiary.bot.utils.exceptions import TaskiqTaskError
from idiotDiary.core.config import Paths
from idiotDiary.core.utils.dates import get_now_isoformat
from idiotDiary.mq.tasks.draw_screenshot import draw_screenshot


def as_render_callback(render_func: RenderFunc) -> OnFinish:
    @inject
    async def _wrapper(
            message: types.Message, manager: DialogManager,
            paths: FromDishka[Paths]
    ):
        async with atf.TemporaryDirectory(dir=paths.temp_folder_path) as tmpdir:
            temp_path = Path(tmpdir)  # noqa
            module_func = f"{render_func.__module__}:{render_func.__name__}"  # noqa
            render_task: AsyncTaskiqTask = await draw_screenshot.kiq(
                module_func=module_func, temp_dir=temp_path,
                **manager.dialog_data
            )
            render_result: TaskiqResult = await render_task.wait_result(
                timeout=120
            )
            if render_result.is_err:
                raise TaskiqTaskError(
                    f"Рендер скриншота функции {module_func} "
                    f"завершился с ошибкой",
                    render_result.error
                )
            photo = types.FSInputFile(
                path=render_result.return_value,
                filename=f"screenshot-{get_now_isoformat()}.png"
            )
            await message.answer_document(document=photo)
            await manager.start(
                state=MainMenuSG.state, mode=StartMode.RESET_STACK
            )

    return cast(OnFinish, _wrapper)
