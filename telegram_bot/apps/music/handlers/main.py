from typing import Optional

from aiogram import Router, F, types
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.context import FSMContext

from common.FSM import CommonFSM
from common.keyboards.start import StartKeyboard
from ..FSM.main import MusicState
from ..keyboards.main import MusicMainKeyboard
from ..utils.audio import BigDurationError

start_music_router = Router(name="start_music")


@start_music_router.message(
    CommonFSM.start,
    F.text == StartKeyboard.Buttons.music,
)
async def music_start(message: types.Message,
                      state: FSMContext,
                      text: Optional[str] = None):
    await state.set_state(MusicState.start)
    await message.answer(
        text=text or "Выберите действие:",
        reply_markup=MusicMainKeyboard.build()
    )


@start_music_router.error(
    ExceptionTypeFilter(BigDurationError),
    F.update.message.as_("message")
)
async def big_duration_audio_error(_: types.ErrorEvent,
                                   message: types.Message,
                                   state: FSMContext):
    return await music_start(
        message=message,
        state=state,
        text="Видео, на которое вы отправили ссылку, идет более 10 минут. По техническим причинам "
             "на данный момент скачивание аудио более 10 минут невозможно."
    )
