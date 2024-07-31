from aiogram import Router, types
from aiogram.filters import Command
from aiogram_dialog import DialogManager, ShowMode
from sqlalchemy.ext.asyncio import AsyncSession

from .main import get_birthdays_text

birthdays_command_router = Router(name="birthday_command")


@birthdays_command_router.message(Command("birthdays"))
async def check_birthdays_command(message: types.Message,
                                  session: AsyncSession,
                                  user_id: int,
                                  dialog_manager: DialogManager):
    message_text = await get_birthdays_text(
        session=session,
        user_id=user_id
    )
    await message.answer(message_text)
    await dialog_manager.update({}, ShowMode.DELETE_AND_SEND)
