import os
import re
import subprocess
import uuid

from yt_dlp import YoutubeDL

from common.utils.decorators import set_async, coro_timer
from .. import settings


@coro_timer(45, exc=TimeoutError)
@set_async
def download_audio(
        url: str,
        from_second: str | None = None,
        to_second: str | None = None,
):
    info_dict = YoutubeDL().extract_info(url, download=False)
    title = info_dict.get('title')
    channel = info_dict.get('channel')
    filename = f"{channel} - {title}" if title and channel else uuid.uuid4().hex

    temp_filename_mp3 = filename + ".mp3"
    temp_filename_m4a = filename + ".m4a"
    file_path_mp3 = settings.TEMP_DIR / temp_filename_mp3
    file_path_mp4 = settings.TEMP_DIR / temp_filename_m4a

    ydl_opts = {
        "extract_audio": True,
        "format": 'bestaudio[ext=mp4]',
        "outtmpl": str(file_path_mp4),
        "external_downloader": "ffmpeg",
    }
    if valid(from_second, to_second):
        ydl_opts["external_downloader_args"] = {'ffmpeg': ["-ss", from_second, "-to", to_second]}

    if not settings.TEMP_DIR.exists():
        settings.TEMP_DIR.mkdir(exist_ok=True)

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    subprocess.run(["ffmpeg", "-i", file_path_mp4, "-acodec", "libmp3lame", file_path_mp3])

    with open(file_path_mp3, "rb") as file:
        audio_bytes = file.read()

    for file in [file_path_mp4, file_path_mp3]:
        if file.is_file():
            os.remove(file)

    return audio_bytes, temp_filename_mp3


def valid(from_second: str | None = None, to_second: str | None = None):
    if from_second is not None and to_second is not None:
        if re.match(settings.TIMECODE_REGEXP, from_second) and re.match(settings.TIMECODE_REGEXP, to_second):
            return True
    return False
