from aiogram import Router

from .handlers.eyed3_editor import music_eyed3_dialog
from .handlers.main import start_music_dialog
from .handlers.yt_downloader import music_yt_dialog

music_router = Router(name="music")
music_router.include_routers(
    start_music_dialog,
    music_yt_dialog,
    music_eyed3_dialog,
)
