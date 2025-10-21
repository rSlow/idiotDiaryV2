from aiogram import Router
from .chat import instagram_reels_download


def setup_chat():
    router = Router(name=__name__)

    router.include_routers(
        instagram_reels_download.setup()
    )

    return router
