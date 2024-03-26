from datetime import datetime

from aiogram import types
from aiogram.enums import ContentType
from aiogram_dialog.widgets.input import MessageInput

from common.buttons import CANCEL_BUTTON
from ..states import VideoNoteFSM
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.text import Const


async def download_video_note(message: types.Message,
                              _: MessageInput,
                              manager: DialogManager):
    await message.delete()

    chat_id = message.chat.id
    dialog_message_id: int = manager.current_stack().last_message_id
    await message.bot.edit_message_text(
        chat_id=chat_id,
        message_id=dialog_message_id,
        text="Видеосообщение принято, обработка..."
    )

    video_note_file_io = await message.bot.download(file=message.video_note.file_id)
    video_note = types.BufferedInputFile(
        file=video_note_file_io.read(),
        filename=f"{datetime.now().isoformat()}.mp4"
    )

    await message.bot.edit_message_text(
        chat_id=chat_id,
        message_id=dialog_message_id,
        text="Видео отправляется..."
    )

    await message.answer_document(document=video_note)
    manager.show_mode = ShowMode.DELETE_AND_SEND


video_note_dialog = Dialog(
    Window(
        Const("Ожидаю кружочек..."),
        MessageInput(
            func=download_video_note,
            content_types=ContentType.VIDEO_NOTE
        ),
        CANCEL_BUTTON,
        state=VideoNoteFSM.state
    )
)
