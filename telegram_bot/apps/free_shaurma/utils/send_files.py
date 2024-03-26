from io import BytesIO
from typing import Callable, Awaitable

from aiogram import types
from aiogram.types import BufferedInputFile
from aiogram_dialog import DialogManager, StartMode

from common.FSM import CommonFSM
from common.utils.functions import get_now
from config.logger import logger

RenderFunc = Callable[..., BytesIO]
OnFinish = Callable[[types.Message, DialogManager], Awaitable]


def render_callback(func: RenderFunc) -> OnFinish:
    async def on_finish(message: types.Message,
                        manager: DialogManager):
        await send_file(
            message=message,
            data=manager.dialog_data,
            render_func=func
        )
        await manager.start(state=CommonFSM.start, mode=StartMode.RESET_STACK)

    return on_finish


async def send_file(message: types.Message,
                    data: dict,
                    render_func: RenderFunc):
    image_io = render_func(**data)
    photo = BufferedInputFile(
        file=image_io.read(),
        filename=f"{get_now():%d_%m_%y__%H_%M_%S}.PNG"
    )
    await message.answer_document(document=photo)
    logger.info(f"[SCREEN] | {message.from_user.id}")
