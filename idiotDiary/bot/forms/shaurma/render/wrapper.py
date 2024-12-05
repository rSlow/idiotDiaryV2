from typing import cast

from aiogram import types
from aiogram.enums import ChatAction
from aiogram_dialog import DialogManager, StartMode

from idiotDiary.bot.forms.shaurma.utils.types import RenderFunc
from idiotDiary.bot.states.start import MainMenuSG
from idiotDiary.bot.utils.dialog_factory import OnFinish
from idiotDiary.bot.utils.taskiq_context import TaskiqContext
from idiotDiary.core.utils.dates import get_now_isoformat
from idiotDiary.mq.tasks.draw_screenshot import draw_screenshot


def as_render_callback(render_func: RenderFunc) -> OnFinish:
    async def _wrapper(message: types.Message, manager: DialogManager):
        module_func = f"{render_func.__module__}:{render_func.__name__}"  # noqa

        async with TaskiqContext(
                task=draw_screenshot, manager=manager,
                error_log_message=f"Рендер скриншота функции {module_func} завершился с ошибкой",
                timeout_message="Превышено время генерации изображения.",
        ) as context:
            await message.bot.send_chat_action(
                chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO
            )
            photo_path = await context.wait_result(
                timeout=120,
                module_func=module_func, temp_dir=context.temp_folder,
                **manager.dialog_data
            )
            photo = types.FSInputFile(
                path=photo_path,
                filename=f"screenshot-{get_now_isoformat()}.png"
            )
            await message.answer_document(document=photo)

        await manager.start(state=MainMenuSG.state, mode=StartMode.RESET_STACK)

    return cast(OnFinish, _wrapper)
