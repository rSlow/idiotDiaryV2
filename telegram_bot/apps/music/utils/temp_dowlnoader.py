from pathlib import Path

from aiofiles import os
from aiogram import Bot


class TempFileDownloader:
    def __init__(self, file_path: Path,
                 bot: Bot,
                 file_id: str):
        self.file_path = file_path
        self.bot = bot
        self.file_id = file_id

    @property
    def parent(self):
        return self.file_path.parent

    async def __aenter__(self):
        if not await os.path.isdir(self.parent):
            await os.mkdir(self.parent)
        await self.bot.download(
            file=self.file_id,
            destination=self.file_path
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if await os.path.isfile(self.file_path):
            await os.remove(self.file_path)
