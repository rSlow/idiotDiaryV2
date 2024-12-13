from aiogram import Router

from idiotDiary.bot.filters.base import set_filter_on_router
from idiotDiary.bot.filters.user import role_filter
from .create import create_sub_dialog
from .current_list import current_subs_dialog
from .edit import sub_edit_dialog
from .main import subs_main_dialog


def setup():
    router = Router(name=__name__)
    set_filter_on_router(router, role_filter("subs"))

    router.include_routers(
        subs_main_dialog,
        current_subs_dialog,
        create_sub_dialog,
        sub_edit_dialog,
    )

    return router
