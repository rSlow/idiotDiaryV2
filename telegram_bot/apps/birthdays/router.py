from aiogram import Router

from .handlers.calendar import calendar_dialog
from .handlers.clear import clear_dialog
from .handlers.main import main_birthday_dialog
from .handlers.notifications import notifications_dialog, clear_notifications_dialog, add_time_notification_dialog
from .handlers.time_correction import time_correction_dialog
from .filters import BirthdaysAllowedFilter

birthdays_router = Router(name="birthdays")
birthdays_router.message.filter(BirthdaysAllowedFilter())

birthdays_router.include_routers(
    main_birthday_dialog,
    clear_dialog,
    time_correction_dialog,
    notifications_dialog,
    clear_notifications_dialog,
    add_time_notification_dialog,
    calendar_dialog,
)
