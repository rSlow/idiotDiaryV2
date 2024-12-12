from urllib.parse import urlparse

from aiogram import types
from aiogram_dialog import DialogManager

from idiotDiary.bot.utils.message import edit_dialog_message
from idiotDiary.bot.utils.taskiq_context import TaskiqContext
from idiotDiary.mq.tasks import subs


async def on_url_success(message: types.Message, _, manager: DialogManager, data: str):
    await message.delete()
    await edit_dialog_message(manager, "Проверка...")
    async with TaskiqContext(
            task=subs.is_url_valid, manager=manager,
            error_user_message="Во время проверки ссылки возникла ошибка. "
                               "Пожалуйста, попробуйте добавить ссылку через некоторое время.",
            timeout_message="Превышено время проверки. Попробуйте повторить чуть позже."
    ) as context:
        parsed_url = urlparse(data)
        request_url = (f"{parsed_url.scheme}://"
                       f"{parsed_url.netloc}"
                       f"{parsed_url.path}"
                       f"?{parsed_url.query}")
        is_url_valid: bool = await context.wait_result(timeout=60, url=request_url)
        if is_url_valid:
            manager.dialog_data["url"] = request_url
            await manager.next()
        else:
            await message.answer(
                f"<a href='{data}'>Ссылка</a> ведет на валидный сайт, но при этом страница "
                f"не содержит списка элементов. Проверьте правильность введенной ссылки.",
                disable_web_page_preview=True
            )
