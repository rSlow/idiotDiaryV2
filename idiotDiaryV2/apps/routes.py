from aiogram import Router

from .admin.router import admin_router
from .birthdays.router import birthdays_router
from .free_shaurma.router import fsh_router
from .music.router import music_router
from .not_working_place.router import nwp_router

apps_router = Router(name="apps")

apps_router.include_routers(
    nwp_router,
    fsh_router,
    birthdays_router,
    music_router,
    admin_router,
)
