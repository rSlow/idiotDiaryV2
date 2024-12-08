from urllib.parse import urlparse

from aiogram import types
from aiogram_dialog import DialogManager

from idiotDiary.bot.utils.message import edit_dialog_message
from idiotDiary.bot.utils.taskiq_context import TaskiqContext
from idiotDiary.mq.tasks.subs import check_url


async def on_url_success(message: types.Message, _, manager: DialogManager, data: str):
    await message.delete()
    await edit_dialog_message(manager, "Проверка...")
    async with TaskiqContext(
            task=check_url, manager=manager,
            error_user_message="Во время проверки ссылки возникла неизвестная ошибка. "
                               "Пожалуйста, попробуйте добавить ссылку через некоторое время."
    ) as context:
        real_url: str | None = await context.wait_result(timeout=30, url=data)
        if real_url is not None:
            parsed_url = urlparse(real_url)
            manager.dialog_data["url"] = str(parsed_url.parent) + "?" + parsed_url.query_string
            await manager.next()
        else:
            await message.answer(
                f"<a href='{data}'>Ссылка</a> ведет на сайт FarPost, но при этом страница "
                f"не содержит списка элементов. Проверьте правильность введенной ссылки."
            )
