from aiogram import Router

from common.filters import BirthdaysAllowedFilter
from .clear import clear_dialog
from .main import main_birthday_dialog
from .notifications import notifications_dialog, clear_notifications_dialog, add_time_notification_dialog
from .time_correction import time_correction_dialog

birthdays_router = Router(name="birthdays")
birthdays_router.message.filter(BirthdaysAllowedFilter())

birthdays_router.include_routers(
    main_birthday_dialog,
    clear_dialog,
    time_correction_dialog,
    notifications_dialog,
    clear_notifications_dialog,
    add_time_notification_dialog,
)
