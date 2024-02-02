import os.path

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from common.FSM import CommonFSM
from common.filters import OwnerFilter, NoKeyboardFilter
from common.keyboards.start import StartKeyboard
from config import settings
from ..FSM.admin import AdminStates
from ..keyboards.admin import AdminKeyboard

admin_router = Router(name="admin")


@admin_router.message(
    AdminStates.confirm_delete_birthdays,
    NoKeyboardFilter(),
)
@admin_router.message(
    CommonFSM.start,
    OwnerFilter(),
    F.text == StartKeyboard.Buttons.admin,
)
async def start_admin(message: types.Message, state: FSMContext):
    await state.set_state(AdminStates.start)

    await message.answer(
        text="Выберите действие:",
        reply_markup=AdminKeyboard.build()
    )


@admin_router.message(
    AdminStates.start,
    F.text == AdminKeyboard.Buttons.get_logs,
)
async def get_logs(message: types.Message):
    files = [
        types.FSInputFile(
            path=filename,
            filename=filename.name
        ) for filename in settings.LOGS_DIR.glob("*.log")
        if os.path.getsize(filename)  # check file is not empty
    ]
    media = [types.InputMediaDocument(media=file) for file in files]
    await message.answer_media_group(media)
