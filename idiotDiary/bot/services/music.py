import uuid
from pathlib import Path

import aiofiles
import aiofiles.tempfile as atf
import eyed3
from aiogram import types, Bot
from aiogram_dialog import DialogManager, ShowMode
from eyed3.id3 import Tag

from idiotDiary.bot.utils.message import edit_dialog_message
from idiotDiary.core.config import Paths


async def initialize_audio_file(message: types.Message, manager: DialogManager):
    bot: Bot = manager.middleware_data["bot"]
    paths: Paths = manager.middleware_data["paths"]

    audio = message.audio
    file_id = audio.file_id
    filename = audio.file_name or f"{uuid.uuid4().hex}.mp3"

    await edit_dialog_message(manager=manager, text="Обработка...")

    async with atf.TemporaryDirectory(dir=paths.temp_folder_path) as temp_dir:
        file_path = Path(temp_dir) / filename
        await bot.download(file=file_id, destination=file_path)
        eyed3_audio = eyed3.load(file_path)
        if eyed3_audio is None:
            await message.answer(
                "Невозможно распознать файл. Попробуйте загрузить другой файл."
            )
            return await manager.done()

        eyed3_tag = eyed3_audio.tag or Tag()
        # eyed3_tag: Tag = eyed3_audio.tag if eyed3_audio.tag is not None else Tag()

        thumbnail = audio.thumbnail.file_id if audio.thumbnail else None
        manager.dialog_data.update({
            "filename": filename,
            "file_id": file_id,
            "album": eyed3_tag.album,
            "title": audio.title,
            "artist": audio.performer,
            "thumbnail": thumbnail
        })

    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.next()


async def set_thumbnail(tag: Tag, image_path: Path):
    for image in tag.images:  # delete all existing
        tag.images.remove(image.description)

    async with aiofiles.open(image_path, "rb") as file:
        file_data = await file.read()
        tag.images.set(
            type_=3,
            img_data=file_data,
            mime_type="image/jpeg"
        )
