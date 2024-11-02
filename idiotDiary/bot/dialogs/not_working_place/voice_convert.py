from aiogram import types, F
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.text import Const, Format

from idiotDiary.bot.states.not_working_place import ConvertVoiceSG
from idiotDiary.bot.utils.message import edit_dialog_message
from idiotDiary.bot.views import buttons as b
from idiotDiary.core.utils.dates import get_now_isoformat

DD_KEY = "voice_filename"


async def convert_voice_message(
        message: types.Message, _, manager: DialogManager
):
    await message.delete()
    await edit_dialog_message(manager=manager, text="Конвертирую...")
    voice_filename = manager.dialog_data.get(DD_KEY)

    voice_file_io = await message.bot.download(message.voice.file_id)
    voice_file = types.BufferedInputFile(
        file=voice_file_io.read(),
        filename=voice_filename or f"voice-message-{get_now_isoformat()}.mp3"
    )
    await message.answer_document(document=voice_file)
    manager.dialog_data.clear()
    manager.show_mode = ShowMode.DELETE_AND_SEND


async def set_voice_file_text(
        message: types.Message, _, manager: DialogManager, text: str
):
    await message.delete()
    manager.dialog_data[DD_KEY] = text + ".mp3"


async def getter(dialog_manager: DialogManager, **__):
    filename = dialog_manager.dialog_data.get(DD_KEY)
    return {"filename": filename}


voice_convert_dialog = Dialog(
    Window(
        Const("Ожидаю голосовое сообщение..."),
        Format(
            "Имя готового файла - <u>{filename}</u>",
            when=F["filename"]
        ),
        Format(
            "Можно отправить перед голосовым текст, "
            "который возьмется за название файла.",
            when=~F["filename"]
        ),
        MessageInput(
            func=convert_voice_message,
            content_types=ContentType.VOICE
        ),
        TextInput(
            id="voice_name",
            on_success=set_voice_file_text
        ),
        b.CANCEL,
        getter=getter,
        state=ConvertVoiceSG.state,
    )
)
