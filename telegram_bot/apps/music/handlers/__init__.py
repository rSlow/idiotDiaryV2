from aiogram import Router

from .main import start_music_router

music_router = Router(name="shazam")
music_router.include_routers(
    start_music_router,
)
