import asyncio
import uuid
from datetime import datetime, time
from pathlib import Path
from typing import Optional

from pytube import StreamQuery, Stream, YouTube

import settings
from exceptions import BigDurationError


def timedelta(_to: time,
              _from: time):
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

    return _to_datetime(_to) - _to_datetime(_from)


async def download(url: str,
                   dir_path: Path,
                   from_time: Optional[time] = None,
                   to_time: Optional[time] = None):
    yt = YouTube(url)
    streams: StreamQuery = await yt.streams
    filtered_streams = streams.filter(only_audio=True).order_by("bitrate")
    audio: Stream = filtered_streams.last()

    url_duration = await yt.length
    title: str = audio.title
    download_url: str = audio.url

    filename = title or uuid.uuid4().hex

    filename_with_ext = filename + ".mp3"
    file_path = dir_path / filename_with_ext

    if from_time and to_time:
        duration = timedelta(to_time, from_time).total_seconds()
    else:
        duration = url_duration
    if duration > 600:
        raise BigDurationError(f"duration of audio {duration} seconds too long")

    ffmpeg_command = ["ffmpeg", "-i", download_url, "-acodec", "libmp3lame"]
    if from_time:
        ffmpeg_command.extend(["-ss", from_time.strftime(settings.TIME_FORMAT)])
    if to_time:
        ffmpeg_command.extend(["-to", to_time.strftime(settings.TIME_FORMAT)])

    ffmpeg_command.append(file_path.as_posix())
    process = await asyncio.subprocess.create_subprocess_exec(*ffmpeg_command)
    await process.wait()

    return file_path
