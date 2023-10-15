from aiogram import Router
from apps.not_working_place.handlers import nwp_router
from apps.free_shaurma.handlers import fsh_router

apps_router = Router(name="apps")

apps_router.include_routers(
    nwp_router,
    fsh_router
)
