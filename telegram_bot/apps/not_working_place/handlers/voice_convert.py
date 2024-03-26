from datetime import datetime

from aiogram import types
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.api.entities import Context
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.text import Const, Format

from common.buttons import CANCEL_BUTTON
from config import settings
from ..states import VoiceFSM

DD_KEY = "VOICE_NAME"


async def convert_voice_message(message: types.Message,
                                _: MessageInput,
                                manager: DialogManager):
    await message.delete()

    chat_id = message.chat.id
    dialog_message_id: int = manager.current_stack().last_message_id
    await message.bot.edit_message_text(
        chat_id=chat_id,
        message_id=dialog_message_id,
        text="Конвертирую..."
    )

    filename = manager.dialog_data.get(DD_KEY, datetime.now().astimezone(settings.TIMEZONE).isoformat())
    voice_file_io = await message.bot.download(file=message.voice.file_id)
    voice_file = types.BufferedInputFile(
        file=voice_file_io.read(),
        filename=f"{filename}.mp3"
    )
    await message.answer_document(document=voice_file)

    manager.dialog_data.clear()
    manager.show_mode = ShowMode.DELETE_AND_SEND


async def set_voice_file_text(message: types.Message,
                              _: ManagedTextInput,
                              manager: DialogManager,
                              text: str):
    await message.delete()
    manager.show_mode = ShowMode.EDIT
    await manager.update({DD_KEY: text})


async def getter(aiogd_context: Context, **__):
    filename = aiogd_context.dialog_data.get(DD_KEY, "")
    placeholder = "Можно отправить перед голосовым текст, который возьмется за название файла."
    return {"filename": f"Название файла: <u>{filename}</u>" if filename else placeholder}


voice_convert_dialog = Dialog(
    Window(
        Const("Ожидаю голосовое сообщение..."),
        Format("{filename}"),
        MessageInput(
            func=convert_voice_message,
            content_types=ContentType.VOICE
        ),
        TextInput(
            id="voice_name",
            on_success=set_voice_file_text
        ),
        CANCEL_BUTTON,
        state=VoiceFSM.state,
        getter=getter
    )
)
