import logging

from aiogram import Router, Dispatcher
from aiogram_dialog import setup_dialogs as setup_aiogram_dialogs

# from . import admin, birthdays, music, not_working_place, shaurma
from . import admin, not_working_place, birthdays
from .main_menu import main_menu

logger = logging.getLogger(__name__)


def setup_dialogs(dp: Dispatcher):
    dialog_router = Router(name=__name__)

    dialog_router.include_router(main_menu)

    dialog_router.include_router(not_working_place.setup())
    dialog_router.include_router(admin.setup())
    dialog_router.include_router(birthdays.setup())
    # dialog_router.include_router(music.setup())
    # dialog_router.include_router(shaurma.setup())

    dp.include_router(dialog_router)

    bg_manager_factory = setup_aiogram_dialogs(dp)
    logger.info("dialogs configured successfully")

    return bg_manager_factory
