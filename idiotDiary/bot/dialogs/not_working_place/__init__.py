from aiogram import Router

from .inn_parser import inn_dialog
from .main import nwp_menu
from .morph import morph_dialog
from .video_note import video_note_dialog
from .voice_convert import voice_convert_dialog
from .zip_pdf import zip_pdf_dialog
from .zip_photos import zip_photos_dialog


def setup():
    router = Router(name=__name__)

    router.include_routers(
        inn_dialog,
        nwp_menu,
        morph_dialog,
        zip_pdf_dialog,
        zip_photos_dialog,
        voice_convert_dialog,
        video_note_dialog,
    )

    return router
