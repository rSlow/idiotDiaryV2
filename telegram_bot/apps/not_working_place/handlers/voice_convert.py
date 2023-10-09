from asyncio import sleep
from datetime import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile
from ..FSM.start import Start
from ..FSM.convert_voice import ConvertVoice
from ..keyboards.main import NotWorkingPlaceKeyboard
from ..keyboards.voice_convert import ConvertVideoKeyboard, ConvertAgainVideoKeyboard

from . import router


@router.message(
    F.text == ConvertAgainVideoKeyboard.Buttons.again,
    ConvertVoice.convert
)
@router.message(
    F.text == NotWorkingPlaceKeyboard.Buttons.convert_voice,
    Start.main
)
async def convert_voice_message_start(message: Message, state: FSMContext):
    await state.set_data({})
    await state.set_state(ConvertVoice.start)

    await message.answer(
        text=f"Ожидаю голосовое сообщение...\n"
             f"Можно отправить перед голосовым текст, который возьмется за название файла.",
        reply_markup=ConvertVideoKeyboard.build()
    )


@router.message(
    F.text,
    ConvertVoice.start,
)
async def set_voice_file_text(message: Message, state: FSMContext):
    await state.update_data({"VOICE_NAME": message.text})

    inf_msg = await message.answer(
        text=f"Название <i>{message.text}</i> принято.",
    )
    await sleep(2)
    await inf_msg.delete()


@router.message(
    F.voice,
    ConvertVoice.start,
)
async def convert_voice_message(message: Message, state: FSMContext):
    await state.set_state(ConvertVoice.convert)

    data = await state.get_data()
    filename = data["VOICE_NAME"]
    if filename is None:
        filename = datetime.now().isoformat()

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
