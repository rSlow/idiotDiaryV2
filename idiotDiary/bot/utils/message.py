import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

logger = logging.getLogger(__name__)


async def delete_message(
        bot: Bot, chat_id: int, message_id: int,
        error_text: str | None = None
) -> bool:
    try:
        return await bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
    except TelegramBadRequest as ex:
        logger.warning(
            error_text.format_map({
                "ex": ex,
                "message_id": message_id,
                "chat_id": chat_id
            })
            if error_text
            else f"Error while deleting message {message_id}: {ex.message}"
        )
