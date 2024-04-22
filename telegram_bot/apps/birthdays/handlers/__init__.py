from aiogram import Router

from .clear import clear_dialog
from .command import birthdays_command_router
from .main import main_birthday_dialog
from .notifications import notifications_dialog, clear_notifications_dialog, add_time_notification_dialog
from .time_correction import time_correction_dialog
from ..filters import BirthdaysAllowedFilter

birthdays_router = Router(name="birthdays")
birthdays_router.message.filter(BirthdaysAllowedFilter())

birthdays_router.include_routers(
    birthdays_command_router,
    main_birthday_dialog,
    clear_dialog,
    time_correction_dialog,
    notifications_dialog,
    clear_notifications_dialog,
    add_time_notification_dialog,
)
