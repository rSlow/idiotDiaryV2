from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from common.buttons import MAIN_MENU_BUTTON
from ..states import MusicMainFSM, YTDownloadFSM, EyeD3FSM

start_music_dialog = Dialog(
    Window(
        Const("Выберите действие:"),
        Start(
            Const("Редактор eyeD3 👁‍🗨"),
            id="eyed3_editor",
            state=EyeD3FSM.wait_file
        ),
        Start(
            Const("Скачать музыку из видео ⬇️"),
            id="music_download",
            state=YTDownloadFSM.url
        ),
        MAIN_MENU_BUTTON,
        state=MusicMainFSM.state
    )
)
