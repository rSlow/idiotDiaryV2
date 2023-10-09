from aiogram import Router
from apps import not_working_place

root_router = Router(name="root")

root_router.include_routers(
    not_working_place.router,
)
