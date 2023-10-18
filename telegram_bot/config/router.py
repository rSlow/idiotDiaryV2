from aiogram import Router
from apps.not_working_place.handlers import nwp_router
from apps.free_shaurma.handlers import fsh_router
from apps.admin.handlers import admin_router
from apps.music.handlers import music_router

apps_router = Router(name="apps")

apps_router.include_routers(
    nwp_router,
    fsh_router,
    admin_router,
    music_router
)
