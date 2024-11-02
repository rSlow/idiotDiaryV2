from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const
from aiohttp import ClientSession
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from idiotDiary.bot.config.models import BotConfig
from idiotDiary.bot.states.not_working_place import MorphFioSG
from idiotDiary.bot.views import buttons as b

MORPH_CASE_ALIASES = {
    "1": "Именительный",
    "2": "Родительный",
    "3": "Дательный",
    "4": "Винительный",
    "5": "Творительный",
    "6": "Предложный",
}


def text_check(text: str):
    text_objects = text.split()
    if len(text_objects) >= 3:
        return text
    raise ValueError


async def morph_fio(text: str, service_url: str):
    async with ClientSession() as session:
        response = await session.post(
            url=service_url + "/fio/all",
            json={"fio": text}
        )
        cased_objects: dict[str, str] = await response.json()
    return cased_objects


@inject
async def text_handler(
        message: types.Message, _, manager: DialogManager, text: str,
        bot_config: FromDishka[BotConfig]
):
    cased_objects = await morph_fio(text, bot_config.morph_service_url)
    message_text = "\n".join([
        f"<b><u>{MORPH_CASE_ALIASES[case_idx]}:</u></b> "
        f"<code>{cased_fio}</code>"
        for case_idx, cased_fio in cased_objects.items()
    ])
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.answer(message_text)


async def error_handler(message: types.Message, _, manager: DialogManager, __):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.answer("Неверный формат ФИО. Попробуйте еще раз.")


morph_dialog = Dialog(
    Window(
        Const(
            "Введите ФИО в формате "
            "<code>Иванов Иван Иванович</code>"
        ),
        TextInput(
            id="morph_data",
            type_factory=text_check,
            on_success=text_handler,  # noqa
            on_error=error_handler
        ),
        b.CANCEL,
        state=MorphFioSG.state
    )
)
