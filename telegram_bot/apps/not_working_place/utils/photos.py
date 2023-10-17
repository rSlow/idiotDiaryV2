import datetime
from io import BytesIO
from typing import BinaryIO

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
import zipfile

from common.utils.stage_gather import stage_gather

PHOTOS = "photos"


async def init_photos_proxy(state: FSMContext):
    await state.update_data({PHOTOS: []})


async def add_photo_file_id(state: FSMContext, file_id: str):
    data = await state.get_data()
    photos = data.get(PHOTOS, [])
    photos.append(file_id)
    await state.update_data({PHOTOS: photos})


async def get_file_id_list(state: FSMContext) -> list[str]:
    data = await state.get_data()
    return data[PHOTOS]


async def clear_file_id_list(state: FSMContext) -> None:
    data = await state.get_data()
    del data["photos"]
    await state.set_data(data)


async def download_photo(file_id: str, bot: Bot):
    file = await bot.get_file(file_id)
    photo_io: BinaryIO = await bot.download_file(file_path=file.file_path)
    return photo_io


async def get_zip_file(file_id_list: list[str], bot: Bot):
    tasks = []
    for i, file_id in enumerate(file_id_list, 1):
        tasks.append(download_photo(file_id=file_id, bot=bot))
    photos_io: list[BinaryIO] = await stage_gather(*tasks)

    zip_io = BytesIO()
    with zipfile.ZipFile(file=zip_io, mode="w") as zip_file:
        for i, photo_io in enumerate(photos_io, 1):
            photo_io.seek(0)
            zip_file.writestr(
                zinfo_or_arcname=f"{i}.jpg",
                data=photo_io.read()
            )
    zip_io.seek(0)
    zip_file = BufferedInputFile(
        file=zip_io.read(),
        filename=f"{datetime.datetime.now().ctime()}.zip"
    )

    return zip_file
