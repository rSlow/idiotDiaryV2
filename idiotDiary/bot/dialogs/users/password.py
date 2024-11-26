from aiogram import F, types
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from idiotDiary.bot.states.users import SetPassword
from idiotDiary.bot.views import buttons as b
from idiotDiary.core.db import dto
from idiotDiary.core.db.dao.user import UserDao
from idiotDiary.core.utils.auth import SecurityProps


@inject
async def user_with_password_getter(user: dto.User, user_dao: FromDishka[UserDao], **__):
    user_with_creds = await user_dao.get_by_tg_id_with_password(user.tg_id)
    return {"has_password": user_with_creds.hashed_password is not None}


@inject
async def set_password(
        message: types.Message, _, manager: DialogManager, data: str,
        dao: FromDishka[UserDao], security: FromDishka[SecurityProps]
):
    hashed_password = security.get_password_hash(data)
    user: dto.User = manager.middleware_data["user"]
    await dao.set_password(user, hashed_password)
    await message.answer("Пароль обновлен.")
    await manager.done()


set_password_dialog = Dialog(
    Window(
        Const(
            text="Введите новый пароль:",
            when=F["has_password"]
        ),
        Const(
            text="Введите пароль:",
            when=~F["has_password"]
        ),
        TextInput(
            id="password",
            type_factory=str,
            on_success=set_password,  # noqa
        ),
        b.CANCEL,
        state=SetPassword.state,
        getter=user_with_password_getter
    )
)
