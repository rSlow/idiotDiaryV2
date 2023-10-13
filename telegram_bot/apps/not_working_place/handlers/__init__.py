from aiogram import Router

from .main import main_nwp_router
from .pack_photos import pack_photos_router
from .video_note import video_note_router
from .voice_convert import voice_convert_router

nwp_router = Router(name="not_working_place")
nwp_router.include_routers(
    main_nwp_router,
    pack_photos_router,
    video_note_router,
    voice_convert_router
)
