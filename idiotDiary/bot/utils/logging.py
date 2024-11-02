import logging

from aiogram import types
from aiogram.types.error_event import ErrorEvent
from aiogram.utils.markdown import html_decoration as hd

from idiotDiary.bot.utils.markdown import get_update_text
from idiotDiary.bot.views.alert import BotAlert


async def send_alert(
        alert: BotAlert, update: types.Update, exception: Exception,
        bot_name: str
):
    await alert(
        f"Получено исключение в боте <u>{bot_name}</u>:\n"
        f"-----\n"
        f"{exception.__class__.__name__}: {hd.quote(repr(exception))}\n"
        f"-----\n"
        f"во время обработки апдейта: {get_update_text(update)}",
    )


def log_bot_error(error: ErrorEvent, logger: logging.Logger, bot_name: str):
    update = error.update
    exception = error.exception
    logger.exception(
        f"Получено исключение в боте {bot_name}: {repr(exception)}, "
        f"во время обработки апдейта {update.model_dump(exclude_none=True)}",
        exc_info=exception,
    )
