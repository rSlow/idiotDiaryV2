from aiogram import Router

from .calendar import calendar_dialog
from .clear import clear_dialog
from .main import main_birthday_dialog
from .notifications import (
    notifications_dialog, add_time_notification_dialog,
    clear_notifications_dialog
)
from .time_correction import time_correction_dialog


def setup():
    router = Router(name=__name__)

    router.include_routers(
        clear_dialog,
        main_birthday_dialog,
        calendar_dialog,
        time_correction_dialog,
        notifications_dialog,
        add_time_notification_dialog,
        clear_notifications_dialog,
    )

    return router
