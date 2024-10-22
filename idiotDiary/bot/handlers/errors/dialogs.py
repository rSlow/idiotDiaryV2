import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent, NoContextError

from idiotDiary.bot.states.start import MainMenuSG

logger = logging.getLogger(__name__)


async def clear_unknown_intent(error: ErrorEvent, bot: Bot):
    assert error.update.callback_query
    assert error.update.callback_query.message
    await bot.edit_message_reply_markup(
        chat_id=error.update.callback_query.message.chat.id,
        message_id=error.update.callback_query.message.message_id,
        reply_markup=None,
    )


async def no_context(
        error: ErrorEvent, bot: Bot, dialog_manager: DialogManager
):
    logger.error("No dialog context found", exc_info=error.exception)
    message = error.update.message or error.update.callback_query.message
    assert message
    if message:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Произошла ошибка бота, мы вынуждены вернуть вас "
                 f"в главное меню, и уже работаем над устранением 🛠"
        )
        await dialog_manager.start(
            MainMenuSG.state, mode=StartMode.RESET_STACK,
            show_mode=ShowMode.DELETE_AND_SEND
        )


def setup(dp: Dispatcher):
    dp.errors.register(
        clear_unknown_intent,
        ExceptionTypeFilter(UnknownIntent)
    )
    dp.errors.register(
        no_context,
        ExceptionTypeFilter(NoContextError)
    )
