from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile

from .main import back_to_main
from ..FSM.start import NWPStartFSM
from ..FSM.video_note import DownloadVideoNoteFSM
from ..keyboards.main import NotWorkingPlaceKeyboard
from ..keyboards.video_note import DownloadVideoKeyboard

video_note_router = Router(name="video_note")


@video_note_router.message(
    F.text == NotWorkingPlaceKeyboard.Buttons.download_video_note,
    NWPStartFSM.main
)
async def download_video_note_start(message: Message, state: FSMContext):
    await state.set_state(DownloadVideoNoteFSM.main)
    await message.answer(
        text="Ожидаю кружочек...",
        reply_markup=DownloadVideoKeyboard.build()
    )


@video_note_router.message(
    F.video_note,
    DownloadVideoNoteFSM.main
)
async def download_video_note(message: Message, state: FSMContext):
    await state.set_state(DownloadVideoNoteFSM.download)
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
