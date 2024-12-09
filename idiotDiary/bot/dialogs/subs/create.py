from aiogram_dialog import DialogManager, ShowMode
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from idiotDiary.bot.forms.subs import SubCreateForm
from idiotDiary.bot.utils.dialog_factory import InputDialogFactory
from idiotDiary.bot.utils.message import edit_dialog_message
from idiotDiary.core.db import dto
from idiotDiary.core.db.dao.subscription import SubscriptionDao
from idiotDiary.core.scheduler.scheduler import ApScheduler


@inject
async def create_subscription(
        _, manager: DialogManager,
        dao: FromDishka[SubscriptionDao], scheduler: FromDishka[ApScheduler]
):
    await edit_dialog_message(manager=manager, text="Обработка...")

    user: dto.User = manager.middleware_data["user"]
    data = manager.dialog_data
    sub = await dao.add(
        dto.Subscription(
            user_id=user.id_,
            url=data["url"], frequency=data["frequency"], name=data["name"]
        )
    )
    scheduler.add_ad_subscription(sub)

    await edit_dialog_message(manager=manager, text="Подписка добавлена.")
    manager.show_mode = ShowMode.SEND
    await manager.done()


create_sub_dialog = InputDialogFactory(
    input_form=SubCreateForm,
    on_finish=create_subscription  # noqa
)
