from aiogram import types
from aiogram.enums import ContentType, ChatAction
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from idiotDiary.bot.states.not_working_place import VideoNoteSG
from idiotDiary.bot.utils.message import edit_dialog_message
from idiotDiary.bot.views import buttons as b
from idiotDiary.core.utils.dates import get_now


async def download_video_note(
        message: types.Message, _, manager: DialogManager
):
    await message.delete()
    await edit_dialog_message(manager=manager, text="Видеосообщение принято, обработка...")
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VOICE)
    video_note_file_io = await message.bot.download(message.video_note.file_id)
    video_note = types.BufferedInputFile(
        file=video_note_file_io.read(),
        filename=f"video-note-{get_now().isoformat()}.mp4"
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
        b.CANCEL,
        state=VideoNoteSG.state
    )
)
