import asyncio
import re
from pathlib import Path
from urllib.parse import urlparse

from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram_dialog import DialogManager
from dishka.integrations.aiogram import inject
from taskiq import TaskiqResult

from idiotDiary.bot.utils.taskiq_context import TaskiqContext
from idiotDiary.bot.views import commands
from idiotDiary.core.config import Paths
from idiotDiary.mq.tasks.reels_download import download_instagram_reel


@inject
async def download_reel_in_chat(
        message: types.Message, command: CommandObject, paths: Paths, dialog_manager: DialogManager,
        **kwargs
):
    if command.args is None:
        no_url_msg = await message.answer(
            text=f"Введите ссылку после /reel, например: \n"
                 f"<code>/reel https://www.instagram.com/reel/DOGmdDojBZ1</code>",
            disable_web_page_preview=True,
        )
        await asyncio.sleep(5)
        await no_url_msg.delete()
        return

    else:
        command_args = command.args.split()
        url = command_args[0]
        parsed_url = urlparse(url)
        reel_id_match = re.match(r"/reel/[\w-]+", parsed_url.path)
        if any((
                "instagram.com" not in parsed_url.netloc,
                not reel_id_match,
        )):
            no_url_msg = await message.answer(
                text=f"Введена невалидная ссылка. Ссылка должна быть вида \n"
                     f"<code>https://www.instagram.com/reel/DOGmdDojBZ1</code>",
                disable_web_page_preview=True,
            )
            await asyncio.sleep(5)
            await no_url_msg.delete()
            return

    reel_id = reel_id_match.group().split("/")[-1]

    reel_download_message = await message.reply("Загрузка...")

    async def _error_download_callback(_res: TaskiqResult, _manager: DialogManager):
        await reel_download_message.delete()
        error_download_msg = await message.reply("Загрузка не удалась. Попробуйте еще раз.")
        await asyncio.sleep(5)
        await error_download_msg.delete()

    async def _timeout_callback(_manager: DialogManager):
        await reel_download_message.delete()
        error_download_msg = await message.reply(
            "Загрузка не удалась - превышено время ожидания. Попробуйте еще раз."
        )
        await asyncio.sleep(5)
        await error_download_msg.delete()

    async with TaskiqContext(
            task=download_instagram_reel, manager=dialog_manager,
            error_log_message="Ошибка загрузки reels",
            error_user_message=None,
            error_callback=_error_download_callback,
            timeout_callback=_timeout_callback
    ) as context:
        reel_file_path: Path = await context.wait_result(
            timeout=30, temp_folder=context.temp_folder, reel_id=reel_id
        )
        await reel_download_message.edit_text("Отправляю видео...")
        video_file = types.FSInputFile(path=reel_file_path)
        await message.reply_video(video=video_file)
        await reel_download_message.delete()


def setup():
    router = Router(name=__name__)

    router.message.register(download_reel_in_chat, Command(commands.REEL_DOWNLOAD))

    return router
