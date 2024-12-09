from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from idiotDiary.bot.forms.subs import SubCreateForm
from idiotDiary.bot.states.subs import SubsMainFSM, CurrentSubsFSM
from idiotDiary.bot.views import buttons

subs_main_dialog = Dialog(
    Window(
        Const("Выберите действие:"),
        Start(
            Const("Текущие подписки"),
            state=CurrentSubsFSM.state,
            id="current"
        ),
        Start(
            Const("Добавить подписку"),
            state=SubCreateForm.first(),
            id="create"
        ),
        buttons.CANCEL,
        state=SubsMainFSM.state
    )
)
