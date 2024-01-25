from aiogram import Router

from .check_birthdays import main_birthday_router
from .notifications import notifications_router
from common.filters import BirthdaysAllowedFilter
from .time_correction import time_correction_router

birthdays_router = Router(name="birthdays")
birthdays_router.message.filter(BirthdaysAllowedFilter())

birthdays_router.include_routers(
    main_birthday_router,
    notifications_router,
    time_correction_router,
)
