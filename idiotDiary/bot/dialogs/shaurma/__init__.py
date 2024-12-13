from aiogram import Router

from idiotDiary.bot.filters.base import set_filter_on_router
from idiotDiary.bot.filters.user import role_filter
from .bank_forms import setup as bank_forms_setup
from .pick_form import pick_fsh_form_dialog


def setup():
    router = Router(name=__name__)
    set_filter_on_router(router, role_filter("shaurma"))

    router.include_routers(
        pick_fsh_form_dialog,
        *bank_forms_setup(),
    )

    return router
