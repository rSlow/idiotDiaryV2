from asyncio import sleep
from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile

from config import settings
from ..FSM.convert_voice import ConvertVoiceFSM
from ..FSM.start import NWPStartFSM
from ..keyboards.main import NotWorkingPlaceKeyboard
from ..keyboards.voice_convert import ConvertVideoKeyboard, ConvertAgainVideoKeyboard

voice_convert_router = Router()


@voice_convert_router.message(
    F.text == ConvertAgainVideoKeyboard.Buttons.again,
    ConvertVoiceFSM.convert
)
@voice_convert_router.message(
    F.text == NotWorkingPlaceKeyboard.Buttons.convert_voice,
    NWPStartFSM.main
)
async def convert_voice_message_start(message: Message,
                                      state: FSMContext):
    await state.set_data({})
    await state.set_state(ConvertVoiceFSM.start)

    await message.answer(
        text=f"Ожидаю голосовое сообщение...\n"
             f"Можно отправить перед голосовым текст, который возьмется за название файла.",
        reply_markup=ConvertVideoKeyboard.build()
    )


@voice_convert_router.message(
    F.text,
    ConvertVoiceFSM.start,
)
async def set_voice_file_text(message: Message,
                              state: FSMContext):
    await state.update_data({"VOICE_NAME": message.text})

    inf_msg = await message.answer(
        text=f"Название <i>{message.text}</i> принято.",
    )
    await sleep(2)
    await inf_msg.delete()


@voice_convert_router.message(
    F.voice,
    ConvertVoiceFSM.start,
)
async def convert_voice_message(message: Message,
                                state: FSMContext):
    await state.set_state(ConvertVoiceFSM.convert)

    data = await state.get_data()
    filename = data.get("VOICE_NAME")
    if filename is None:
        filename = datetime.now().astimezone(settings.TIMEZONE).isoformat()

    voice_file_io = await message.bot.download(
        file=message.voice.file_id
    )
    voice_file = BufferedInputFile(
        file=voice_file_io.read(),
        filename=f"{filename}.mp3"
    )
    await message.answer_document(
        document=voice_file
    )
    await message.answer(
        text="Что делаем дальше?",
        reply_markup=ConvertAgainVideoKeyboard.build()
    )
