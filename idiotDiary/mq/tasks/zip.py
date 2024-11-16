import zipfile
from pathlib import Path

from idiotDiary.core.utils.dates import get_now
from idiotDiary.mq.broker import broker


@broker.task
async def zip_files_in_folder(folder_path: Path):
    zip_filename = get_now().isoformat() + ".zip"
    files_to_zip: list[Path] = [*folder_path.glob("*.*")]
    # to prevent trying to zip self zip file (glob is lazy generator)
    with zipfile.ZipFile(file=folder_path / zip_filename, mode="w") as zip_file:
        for file in files_to_zip:
            zip_file.write(file, arcname=file.name)
    return folder_path / zip_filename
