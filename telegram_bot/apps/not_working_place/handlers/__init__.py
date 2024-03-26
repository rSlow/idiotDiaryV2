from aiogram import Router

from .inn_parser import inn_dialog
from .main import nwp_menu
from .morph import morph_dialog
from .pack_photos import pack_dialog
from .video_note import video_note_dialog
from .voice_convert import voice_convert_dialog

nwp_router = Router(name="not_working_place")
nwp_router.include_routers(
    nwp_menu,
    pack_dialog,
    morph_dialog,
    video_note_dialog,
    voice_convert_dialog,
    inn_dialog
)
