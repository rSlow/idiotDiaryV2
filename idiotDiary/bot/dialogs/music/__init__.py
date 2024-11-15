from aiogram import Router

from .eyed3_edit import eyed3_edit_dialog
from .main import start_music_dialog
from .youtube_download import download_audio_dialog


def setup():
    router = Router(name=__name__)

    router.include_routers(
        start_music_dialog,
        eyed3_edit_dialog,
        download_audio_dialog
    )

    return router
