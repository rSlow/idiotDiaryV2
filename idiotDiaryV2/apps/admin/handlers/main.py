import os.path

from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from common.buttons import MAIN_MENU_BUTTON
from config import settings
from ..FSM.admin import AdminFSM


async def get_logs(callback: types.CallbackQuery,
                   _: Button,
                   manager: DialogManager):
    files = [
        types.FSInputFile(
            path=filename,
            filename=filename.name
        ) for filename in settings.LOGS_DIR.glob("*.log")
        if os.path.getsize(filename)  # check file is not empty
    ]
    media = [types.InputMediaDocument(media=file) for file in files]
    if not media:
        await callback.answer("Нет файлов логов :(")
    else:
        await callback.message.answer_media_group(media)
        manager.show_mode = ShowMode.DELETE_AND_SEND


admin_main_dialog = Dialog(
    Window(
        Const("Выберите действие:"),
        Button(
            Const("Файлы логов"),
            id="logs",
            on_click=get_logs
        ),
        MAIN_MENU_BUTTON,
        state=AdminFSM.state
    )
)
