import html

from aiogram import types, F
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Group, ManagedCheckbox, Row
from aiogram_dialog.widgets.text import Const, Format, Case
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from idiotDiary.bot.forms.subs.type_factory import frequency_validator
from idiotDiary.bot.states.subs import SubMenu
from idiotDiary.bot.utils.dialog_factory import choice_window_factory
from idiotDiary.bot.views import buttons
from idiotDiary.bot.views.types.data_checkbox import DataCheckbox
from idiotDiary.core.db.dao.subscription import SubscriptionDao
from idiotDiary.core.scheduler.scheduler import ApScheduler

EDIT_MENU = SwitchTo(
    text=Const("Назад ◀"),
    id="__back__",
    state=SubMenu.main
)


@inject
async def sub_main_getter(
        dialog_manager: DialogManager, sub_dao: FromDishka[SubscriptionDao], **__
):
    sub_id = dialog_manager.start_data["sub_id"]
    subscription = await sub_dao.get(sub_id)
    dialog_manager.dialog_data["sub_is_active"] = subscription.is_active
    subscription.url = html.unescape(subscription.url)
    return {"subscription": subscription}


@inject
async def toggle_is_active(
        _, checkbox: ManagedCheckbox, manager: DialogManager,
        dao: FromDishka[SubscriptionDao], scheduler: FromDishka[ApScheduler]
):
    sub_id: int = manager.start_data["sub_id"]
    updated_sub_is_active: bool = checkbox.is_checked()
    sub = await dao.set_is_active(sub_id, updated_sub_is_active)
    if updated_sub_is_active:
        scheduler.add_ad_subscription(sub)
    else:
        scheduler.remove_ad_subscription(sub.id_)
    await manager.update({}, ShowMode.EDIT)


sub_main_window = Window(
    Format("Подписка <u>{subscription.name}</u>"),
    Format("- <a href='{subscription.url}'>ссылка</a>"),
    Case(
        {True: Const("- активна ✅"), ...: Const("- не активна ❌")},
        selector=F["subscription"].is_active
    ),
    Format("- раз в {subscription.frequency} секунд"),
    Group(
        SwitchTo(
            Const("Название"),
            id="name",
            state=SubMenu.name
        ),
        SwitchTo(
            Const("Частота обновления ⏳"),
            id="frequency",
            state=SubMenu.frequency
        ),
        DataCheckbox(
            checked_text=Const("Активна ✅"),
            unchecked_text=Const("Не активна ❌"),
            id="is_active",
            data_getter="sub_is_active",
            on_state_changed=toggle_is_active  # noqa
        ),
        SwitchTo(
            Const("Удалить 🗑"),
            id="delete",
            state=SubMenu.delete
        ),
        width=2
    ),
    buttons.CANCEL,
    state=SubMenu.main,
    getter=sub_main_getter
)


@inject
async def set_name(
        message: types.Message, _, manager: DialogManager, name: str,
        dao: FromDishka[SubscriptionDao]
):
    await message.delete()
    manager.show_mode = ShowMode.EDIT
    sub_id: int = manager.start_data["sub_id"]
    sub = await dao.get(sub_id)
    if name != sub.name:
        await dao.set_name(sub_id, name)
    await manager.switch_to(SubMenu.main)


sub_name_window = Window(
    Format("Текущее название: <code>{subscription.name}</code>"),
    Const("\nВведите новое название:"),
    TextInput(
        id="name",
        on_success=set_name  # noqa
    ),
    Row(
        EDIT_MENU,
        buttons.MAIN_MENU,
    ),
    state=SubMenu.name,
    getter=sub_main_getter,
)


@inject
async def set_frequency(
        message: types.Message, _, manager: DialogManager, frequency: int,
        dao: FromDishka[SubscriptionDao], scheduler: FromDishka[ApScheduler]
):
    await message.delete()
    manager.show_mode = ShowMode.EDIT
    sub_id: int = manager.start_data["sub_id"]
    sub = await dao.get(sub_id)
    if frequency != sub.frequency:
        updated_sub = await dao.set_frequency(sub_id, frequency)
        scheduler.update_user_ad_subscriptions(updated_sub)

    await manager.switch_to(SubMenu.main)


async def on_error_frequency(message: types.Message, _, manager: DialogManager, error: ValueError):
    await message.delete()
    await message.answer(error.args[0])
    manager.show_mode = ShowMode.DELETE_AND_SEND


sub_frequency_window = Window(
    Format("Текущее значение частоты обновления: {subscription.frequency} секунд\n"),
    Const("Значение частоты обновления должно быть больше или равно 30 секундам."),
    Const("Введите новую частоту обновления (в секундах):"),
    TextInput(
        id="frequency",
        type_factory=frequency_validator,
        on_success=set_frequency,  # noqa
        on_error=on_error_frequency
    ),
    Row(
        EDIT_MENU,
        buttons.MAIN_MENU,
    ),
    state=SubMenu.frequency,
    getter=sub_main_getter
)


@inject
async def delete_sub(
        callback: types.CallbackQuery, _, manager: DialogManager,
        dao: FromDishka[SubscriptionDao], scheduler: FromDishka[ApScheduler]
):
    await callback.message.edit_text("Удаление...")

    sub_id: int = manager.start_data["sub_id"]
    await dao.delete(sub_id)
    scheduler.remove_ad_subscription(sub_id)

    await callback.message.edit_text("Удаление завершено!")
    manager.show_mode = ShowMode.SEND
    await manager.done()


delete_sub_window = choice_window_factory(
    Format("Удалить подписку <u>{subscription.name}</u>?"),
    state=SubMenu.delete,
    back_state=SubMenu.main,
    on_click=delete_sub,  # noqa
    getter=sub_main_getter
)

sub_edit_dialog = Dialog(
    sub_main_window,
    sub_name_window,
    sub_frequency_window,
    delete_sub_window,
)
