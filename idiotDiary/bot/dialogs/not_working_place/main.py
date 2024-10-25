from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, ScrollingGroup
from aiogram_dialog.widgets.text import Const

from idiotDiary.bot.states.not_working_place import ImagesZipSG, MorphFioSG, \
    VideoNoteSG, ConvertVoiceSG, INNParserSG, ZipPdfSG
from idiotDiary.bot.views import buttons as b

nwp_menu = Dialog(
    Window(
        Const("(не)рабочая площадка. Выберите действие:"),
        ScrollingGroup(Start(
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
            # Start(
            #     Const("Стикерная 📑"),
            #     id="stickers",
            #     state=StickersFSM.state
            # ),
            Start(
                Const("Слияние PDF 📄"),
                id="stickers",
                state=ZipPdfSG.state
            ),
            id="subs_scroll",
            width=1,
            height=4,
            hide_on_single_page=True,
        ),
        b.MAIN_MENU,
        state=NWPStartFSM.state,
    )
)
