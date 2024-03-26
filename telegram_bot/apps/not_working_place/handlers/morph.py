from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.text import Const
from aiohttp import ClientSession

from common.buttons import CANCEL_BUTTON
from .. import settings
from ..states import MorphFIOFSM


def text_check(text: str):
    text_objects = text.split()
    if len(text_objects) >= 3:
        return text
    raise ValueError


async def morph_fio(text: str):
    async with ClientSession() as session:
        response = await session.post(
            url=settings.MORPH_URL,
            json={"fio": text}
        )
        cased_objects: dict[str, str] = await response.json()
    return cased_objects


async def text_handler(message: types.Message,
                       _: ManagedTextInput,
                       manager: DialogManager,
                       text: str):
    cased_objects = await morph_fio(text)
    message_text = "\n".join([
        f"<b><u>{settings.MORPH_CASE_ALIASES[case_idx]}:</u></b> <code>{cased_fio}</code>"
        for case_idx, cased_fio in cased_objects.items()
    ])
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.answer(message_text)


async def error_handler(message: types.Message,
                        _: ManagedTextInput,
                        manager: DialogManager,
                        __: ValueError):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.answer("Неверный формат ФИО. Попробуйте еще раз.")


morph_dialog = Dialog(
    Window(
        Const("Введите ФИО в формате <code>Иванов Иван Иванович</code>"),
        TextInput(
            id="morph_data",
            type_factory=text_check,
            on_success=text_handler,
            on_error=error_handler
        ),
        CANCEL_BUTTON,
        state=MorphFIOFSM.state
    )
)
