import tempfile
import uuid
from datetime import datetime, time
from pathlib import Path
from typing import Optional

from common.utils.decorators import to_async_thread
from yt_dlp import YoutubeDL

from .. import settings
from ..exceptions import BigDurationError
from ..schemas import DownloadResult


def _to_datetime(t: time):
    return datetime(
        year=1900,
        month=1,
        day=1,
        hour=t.hour,
        minute=t.minute,
        second=t.second,
        microsecond=t.microsecond,
        tzinfo=t.tzinfo,
        fold=t.fold
    )


def _get_timedelta(
        _to: time,
        _from: time):
    return _to_datetime(_to) - _to_datetime(_from)


@to_async_thread
def download_audio(url: str,
                   root_temp_path: Path,
                   from_time: Optional[time] = None,
                   to_time: Optional[time] = None):
    root_temp_path.mkdir(exist_ok=True)

    req_dict: dict = YoutubeDL({"playlist_items": "1"}).extract_info(
        url=url,
        download=False
    )
    if req_dict.get("entries") is not None:
        info_dict = req_dict["entries"][0]
    else:
        info_dict = req_dict

    url_duration = info_dict.get('duration')
    title = info_dict.get('title')
    channel = info_dict.get('channel')
    filename = f"{channel} - {title}" if title and channel else uuid.uuid4().hex

    with tempfile.TemporaryDirectory(dir=root_temp_path) as temp_dir:
        temp_path = Path(temp_dir)

        filename_with_ext = filename + ".mp3"
        downloaded_file_path = temp_path / filename_with_ext

        ydl_opts: dict = {
            "extract_audio": True,
            "format": 'bestaudio[ext=mp4]',
            "outtmpl": downloaded_file_path.resolve().as_posix(),
            "external_downloader": "ffmpeg",
        }
        if from_time and to_time:
            duration = _get_timedelta(to_time, from_time).total_seconds()
        else:
            duration = url_duration
        if duration > 600:
            raise BigDurationError(
                f"duration of audio {duration} seconds too long")

        ffmpeg_options = ydl_opts.setdefault("external_downloader_args",
                                             {}).setdefault("ffmpeg", [])
        if from_time:
            ffmpeg_options.extend(
                ["-ss", from_time.strftime(settings.STRFTIME_FORMAT)])
        if to_time:
            ffmpeg_options.extend(
                ["-to", to_time.strftime(settings.STRFTIME_FORMAT)])

        ffmpeg_options.extend(["-acodec", "libmp3lame"])

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(info_dict["original_url"])

        with open(downloaded_file_path, "rb") as file:
            audio_bytes = file.read()

    return DownloadResult(
        data=audio_bytes,
        filename=downloaded_file_path.name
    )
