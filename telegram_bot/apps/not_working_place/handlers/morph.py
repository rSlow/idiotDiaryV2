from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession

from common.keyboards.base import CancelKeyboard
from .. import settings
from ..FSM.morph import MorphFIOFSM
from ..FSM.start import NWPStartFSM
from ..keyboards.main import NotWorkingPlaceKeyboard

morph_router = Router(name="morph")


@morph_router.message(
    NWPStartFSM.main,
    F.text == NotWorkingPlaceKeyboard.Buttons.morph,
)
async def morph_fio_start(message: types.Message,
                          state: FSMContext):
    await state.set_state(MorphFIOFSM.morph)

    await message.answer(
        text="Введите ФИО в формате <code>Иванов Иван Иванович</code>",
        reply_markup=CancelKeyboard.build(),
    )


@morph_router.message(
    MorphFIOFSM.morph,
    F.text.as_("fio"),
)
async def morph_fio(message: types.Message,
                    fio: str):
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
