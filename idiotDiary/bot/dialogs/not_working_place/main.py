from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, ScrollingGroup
from aiogram_dialog.widgets.text import Const

from idiotDiary.bot.states.not_working_place import (
    ImagesZipSG, MorphFioSG, VideoNoteSG, ConvertVoiceSG, INNParserSG, ZipPdfSG,
    NwpMainSG
)
from idiotDiary.bot.views import buttons as b

nwp_menu = Dialog(
    Window(
        Const("(не)рабочая площадка. Выберите действие:"),
        ScrollingGroup(
            Start(
                Const("Запаковать 💼"),
                id="pack",
                state=ImagesZipSG.state,
            ),
            Start(
                Const("Склонения 💬"),
                id="morph",
                state=MorphFioSG.state,
            ),
            Start(
                Const("Скачать кружочек 📹"),
                id="download_video_note",
                state=VideoNoteSG.state,
            ),
            Start(
                Const("Конвертировать голосовое 🎤"),
                id="convert_voice",
                state=ConvertVoiceSG.state,
            ),
            Start(
                Const("Узнать ИНН 📇"),
                id="inn_parse",
                state=INNParserSG.state,
            ),
            Start(
                Const("Слияние PDF 📄"),
                id="zip_pdf",
                state=ZipPdfSG.state
            ),
            id="categories_scroll",
            width=1,
            height=4,
        ),
        b.MAIN_MENU,
        state=NwpMainSG.state,
    )
)
