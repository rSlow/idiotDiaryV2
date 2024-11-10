from aiogram import Router

from .bank_forms import setup as bank_forms_setup
from .pick_form import pick_fsh_form_dialog


def setup():
    router = Router(name=__name__)

    router.include_routers(
        pick_fsh_form_dialog,
        *bank_forms_setup(),
    )

    return router
