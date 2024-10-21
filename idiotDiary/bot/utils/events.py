from datetime import datetime

import pytz
from aiogram import types as t
from aiogram_dialog.utils import CB_SEP

from idiotDiary.core.data.db import dto


def from_message(message: t.Message):
    return dto.LogEvent(
        type_="message",
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        content_type=message.content_type,
        dt=message.date,
        data=message.text
    )


def from_callback_query(callback: t.CallbackQuery):
    dt = datetime.now(tz=pytz.UTC)
    chat_id = callback.message.chat.id
    if isinstance(callback.message, t.InaccessibleMessage):
        return dto.LogEvent(
            type_="inaccessible_callback_query",
            chat_id=chat_id,
            dt=dt
        )
    if callback.data and CB_SEP in callback.data:
        data = callback.data.split(CB_SEP, maxsplit=1)[1]
    else:
        data = callback.data

    return dto.LogEvent(
        type_="callback_query",
        user_id=callback.from_user.id,
        chat_id=chat_id,
        dt=dt,
        data=data
    )
