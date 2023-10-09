from datetime import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile

from . import router
from .main import back_to_main
from ..FSM.start import Start
from ..FSM.video_note import DownloadVideoNote
from ..keyboards.main import NotWorkingPlaceKeyboard
from ..keyboards.video_note import DownloadVideoKeyboard


@router.message(
    F.text == NotWorkingPlaceKeyboard.Buttons.download_video_note,
    Start.main
)
async def download_video_note_start(message: Message):
    await DownloadVideoNote.main.set()
    await message.answer(
        text="Ожидаю кружочек...",
        reply_markup=DownloadVideoKeyboard.build()
    )


@router.message(
    F.video_note,
    DownloadVideoNote.main
)
async def download_video_note(message: Message, state: FSMContext):
    await DownloadVideoNote.download.set()
    receive_message = await message.answer("Видеосообщение принято, обработка...")
    video_note_file_io = await message.bot.download(
        file=message.video_note.file_id
    )
    video_note = BufferedInputFile(
        file=video_note_file_io.read(),
        filename=f"{datetime.now().isoformat()}.mp4"
    )
    await receive_message.delete()
    send_message = await message.answer("Видео отправляется...")
    await message.answer_document(
        document=video_note
    )
    await send_message.delete()
    await back_to_main(
        message=message,
        state=state
    )
