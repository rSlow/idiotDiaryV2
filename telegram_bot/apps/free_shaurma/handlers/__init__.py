from aiogram import Router

from .main import start_fsh_router
from .bank_handler import bank_router

fsh_router = Router(name="free_shaurma")

fsh_router.include_routers(
    start_fsh_router,
    bank_router
)
