from aiogram import Router

from .handlers.bank_handler import get_fsh_dialogs
from .handlers.main import start_fsh_dialog

fsh_router = Router(name="free_shaurma")

fsh_router.include_routers(
    start_fsh_dialog,
    *get_fsh_dialogs(),
)
