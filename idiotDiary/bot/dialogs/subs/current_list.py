from operator import itemgetter

from aiogram import F
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Format, Const, Case
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from idiotDiary.bot.forms.subs import SubCreateForm
from idiotDiary.bot.states.subs import SubMenu, CurrentSubsFSM
from idiotDiary.bot.views import buttons
from idiotDiary.core.db import dto
from idiotDiary.core.db.dao.subscription import SubscriptionDao


@inject
async def current_subs_getter(user: dto.User, sub_dao: FromDishka[SubscriptionDao], **__):
    subs = await sub_dao.get_all_user_subscriptions(user.id_)
    subs_buttons = [(sub.id, sub.name, sub.is_active) for sub in subs]
    return {
        "subs": subs_buttons,
        "subs_count": len(subs),
        "active_subs_count": len([*filter(lambda x: x.is_active, subs)])
    }


async def on_sub_click(_, __, dialog_manager: DialogManager, data: str):
    await dialog_manager.start(state=SubMenu.main, data={"sub_id": int(data)})


def item_data_selector(pos: int):
    def inner(data: dict, _: Case, __: DialogManager):
        return data["item"][pos]

    return inner


current_subs_dialog = Dialog(
    Window(
        Format("Текущих подписок: {subs_count}"),
        Format("Активных подписок: {active_subs_count}"),
        ScrollingGroup(
            Select(
                text=Case(
                    texts={
                        True: Format('✅ {item[1]}'),
                        False: Format('❌ {item[1]}'),
                    },
                    selector=item_data_selector(2)
                ),
                item_id_getter=itemgetter(0),
                id="subs",
                items="subs",
                on_click=on_sub_click,
            ),
            id="subs_scroll",
            width=1,
            height=4,
            hide_on_single_page=True,
            when=F["subs"]
        ),
        Start(
            text=Const("Добавить подписку"),
            id="add_sub",
            state=SubCreateForm.first(),
            when=~F["subs"]
        ),
        buttons.CANCEL,
        state=CurrentSubsFSM.state,
        getter=current_subs_getter
    )
)
