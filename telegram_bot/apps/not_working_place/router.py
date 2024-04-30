from aiogram import Router

from .handlers.inn_parser import inn_dialog
from .handlers.main import nwp_menu
from .handlers.morph import morph_dialog
from .handlers.pack_photos import pack_dialog
from .handlers.video_note import video_note_dialog
from .handlers.voice_convert import voice_convert_dialog

nwp_router = Router(name="not_working_place")
nwp_router.include_routers(
    nwp_menu,
    pack_dialog,
    morph_dialog,
    video_note_dialog,
    voice_convert_dialog,
    inn_dialog
)
