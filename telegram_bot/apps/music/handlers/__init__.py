from aiogram import Router

from .main import start_music_router
from .yt_downloader import music_yt_router
from .eyed3_editor import music_eyed3_router

music_router = Router(name="shazam")
music_router.include_routers(
    start_music_router,
    music_yt_router,
    music_eyed3_router,
)
