from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from common.buttons import MAIN_MENU_BUTTON
from ..states import VoiceFSM, StickersFSM
from ..states import ImagesZipFSM
from ..states import INNParserFSM
from ..states import MorphFIOFSM
from ..states import NWPStartFSM
from ..states import VideoNoteFSM

nwp_menu = Dialog(
    Window(
        Const("(не)рабочая площадка. Выберите действие:"),
        Start(
            Const("Запаковать 💼"),
            id="pack",
            state=ImagesZipFSM.state,
        ),
        Start(
            Const("Склонения 💬"),
            id="morph",
            state=MorphFIOFSM.state,
        ),
        Start(
            Const("Скачать кружочек 📹"),
            id="download_video_note",
            state=VideoNoteFSM.state,
        ),
        Start(
            Const("Конвертировать голосовое 🎤"),
            id="convert_voice",
            state=VoiceFSM.state,
        ),
        Start(
            Const("Узнать ИНН 📇"),
            id="inn_parse",
            state=INNParserFSM.state,
        ),
        Start(
            Const("Стикерная 📑"),
            id="stickers",
            state=StickersFSM.state
        ),
        MAIN_MENU_BUTTON,
        state=NWPStartFSM.state,
    )
)
