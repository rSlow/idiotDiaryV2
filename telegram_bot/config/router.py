from aiogram import Router
from apps import not_working_place

apps_router = Router(name="apps")

apps_router.include_routers(
    not_working_place.nwp_router,
    # free_shaurma.fsh_router
)
