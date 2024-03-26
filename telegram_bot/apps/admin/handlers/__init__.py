from aiogram import Router

from .main import admin_main_dialog

admin_router = Router(name="admin")
admin_router.include_routers(
    admin_main_dialog
)
