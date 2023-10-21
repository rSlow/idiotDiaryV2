from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession

from common.keyboards.base import CancelKeyboard
from config import settings
from ..FSM.morph import MorphFIO
from ..FSM.start import Start
from ..keyboards.main import NotWorkingPlaceKeyboard

morph_router = Router(name="morph")


@morph_router.message(
    F.text == NotWorkingPlaceKeyboard.Buttons.morph,
    Start.main

)
async def morph_fio_start(message: types.Message, state: FSMContext):
    await state.set_state(MorphFIO.morph)

    await message.answer(
        text="Введите ФИО в формате <code>Иванов Иван Иванович</code>",
        reply_markup=CancelKeyboard.build(),
    )


@morph_router.message(
    F.text.as_("fio"),
    MorphFIO.morph
)
async def morph_fio(message: types.Message, fio: str):
    async with ClientSession() as session:
        response = await session.post(
            url=settings.MORPH_URL,
            json={"fio": fio}
        )
        cased_objects: dict[str, str] = await response.json()

    message_text = "\n".join([
        f"<b><u>{settings.MORPH_CASE_ALIASES[case_idx]}:</u></b> <code>{cased_fio}</code>"
        for case_idx, cased_fio in cased_objects.items()
    ])
    await message.answer(
        text=message_text,
        reply_markup=CancelKeyboard.build()
    )
