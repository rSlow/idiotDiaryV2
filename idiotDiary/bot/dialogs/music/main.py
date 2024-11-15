from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from idiotDiary.bot.states.music import MusicMainSG, Eyed3EditSG, YTDownloadSG
from idiotDiary.bot.views import buttons as b

start_music_dialog = Dialog(
    Window(
        Const("Выберите действие:"),
        Start(
            Const("Редактор eyeD3 👁‍🗨"),
            id="eyed3_editor",
            state=Eyed3EditSG.get_file
        ),
        Start(
            Const("Скачать музыку из видео ⬇️"),
            id="music_download",
            state=YTDownloadSG.url
        ),
        b.MAIN_MENU,
        state=MusicMainSG.state
    )
)
