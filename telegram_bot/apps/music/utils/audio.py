import os
import re
import subprocess
import uuid
from datetime import timedelta, datetime
from typing import Optional

from yt_dlp import YoutubeDL

from common.utils.decorators import set_async
from .. import settings


class BigDurationError(MemoryError):
    pass


@set_async
def download_audio(
        url: str,
        from_second: str | None = None,
        to_second: str | None = None,
):
    info_dict = YoutubeDL().extract_info(url, download=False)
    url_duration = info_dict.get('duration')
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
        "outtmpl": file_path_mp4.as_posix(),
        "external_downloader": "ffmpeg",
    }
    timecodes = TimecodeValidator(from_second, to_second)
    duration = timecodes.time_interval.seconds if timecodes.has_timecodes else url_duration
    if duration > 600:
        raise BigDurationError

    if timecodes.has_timecodes:
        ydl_opts["external_downloader_args"] = {'ffmpeg': ["-ss", timecodes.from_second, "-to", timecodes.to_second]}

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


class TimeValidationError(TypeError):
    def __init__(self, value: Optional[str] = None):
        super().__init__(f"timecode{' value' if value is not None else 's'} is unvalidated")


class TimecodeValidator:
    def __init__(self,
                 from_second: str | None = None,
                 to_second: str | None = None):
        self.from_second = from_second
        self.to_second = to_second

        if type(from_second) is not type(to_second):
            raise TypeError("you cant determine only one of 'from_second' and 'to_second'")

        if self.has_timecodes and not self.is_valid:
            raise TimeValidationError

    @staticmethod
    def is_match(value: str, is_short: bool = False) -> bool:
        pattern = [settings.TIMECODE_REGEXP, settings.SHORT_TIMECODE_REGEXP][is_short]
        if re.match(pattern, value):
            return True
        return False

    @property
    def is_valid(self) -> bool:
        if self.has_timecodes:
            if self.is_match(self.from_second) and self.is_match(self.to_second):
                return True
        return False

    def get_dt_obj(self, value: str) -> datetime:
        if self.is_match(value, is_short=True):
            return datetime.strptime(
                value, settings.STRFTIME_SHORT_FORMAT
            )
        elif self.is_match(value):
            return datetime.strptime(
                value, settings.STRFTIME_FORMAT
            )
        else:
            raise TimeValidationError(value)

    @property
    def has_timecodes(self):
        return self.from_second is not None and self.to_second is not None

    @property
    def time_interval(self) -> timedelta:
        from_time = self.get_dt_obj(self.from_second)
        to_time = self.get_dt_obj(self.to_second)
        return to_time - from_time
