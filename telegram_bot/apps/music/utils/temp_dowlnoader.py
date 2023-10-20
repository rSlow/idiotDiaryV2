import os
from pathlib import Path

from aiogram import Bot, types


class TempFileDownloader:
    def __init__(self, file_path: Path, bot: Bot, file_id: str, message_to_del: types.Message | None = None):
        self.file_path = file_path
        self.bot = bot
        self.file_id = file_id
        self.message_to_del = message_to_del

    @property
    def parent(self):
        return self.file_path.parent

    async def __aenter__(self):
        if not os.path.isdir(self.parent):
            os.mkdir(self.parent)
        await self.bot.download(
            file=self.file_id,
            destination=self.file_path
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
        if self.message_to_del:
            await self.message_to_del.delete()
