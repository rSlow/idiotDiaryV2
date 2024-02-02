from aiogram import Router

from .bank_handler import bank_router
from .main import start_fsh_router

fsh_router = Router(name="free_shaurma")

fsh_router.include_routers(
    start_fsh_router,
    bank_router
)
