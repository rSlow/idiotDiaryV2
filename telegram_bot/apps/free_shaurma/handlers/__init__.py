from aiogram import Router

from .bank_handler import get_fsh_dialogs
from .main import start_fsh_dialog, test_fsh_router

fsh_router = Router(name="free_shaurma")

fsh_router.include_routers(
    start_fsh_dialog,
    *get_fsh_dialogs(),
)
