from aiogram import Router

from .main import admin_main_dialog
from .roles.add_user import add_user_to_role_dialog
from .roles.create import create_role_dialog
from .roles.role import role_dialog
from .roles.start import role_manager_start_dialog


def setup():
    router = Router(name=__name__)

    router.include_routers(
        admin_main_dialog,
        add_user_to_role_dialog,
        create_role_dialog,
        role_dialog,
        role_manager_start_dialog,
    )

    return router
