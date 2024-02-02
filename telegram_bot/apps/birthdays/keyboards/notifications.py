from typing import Sequence

from common.keyboards.base import BaseReplyKeyboardBuilder
from config import formats
from ..ORM.notifications import NotificationTime


class BirthdaysNotificationsKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        add = "Добавить время ➕"
        clear = "Очистить все 🗑"

    buttons_list = [
        Buttons.add,
        Buttons.clear,
    ]

    @classmethod
    def build(cls,
              notifications: Sequence[NotificationTime] | None = None,
              **kwargs):
        if notifications is None:
            notifications = []

        buttons_list = [f"{notification.time:{formats.TIME_FORMAT}} ❌"
                        for notification in notifications]
        buttons_list.extend(cls.buttons_list)
        return super().build(
            markup_args={"buttons_list": buttons_list}
        )
