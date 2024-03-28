from aiogram import Router

from .eyed3_editor import music_eyed3_dialog
from .main import start_music_dialog
from .yt_downloader import music_yt_dialog

music_router = Router(name="shazam")
music_router.include_routers(
    start_music_dialog,
    music_yt_dialog,
    music_eyed3_dialog,
)
