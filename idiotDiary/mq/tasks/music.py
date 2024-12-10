import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from PIL import Image, ImageOps
from yt_dlp import YoutubeDL

from idiotDiary.bot.utils.exceptions.music import BigDurationError
from idiotDiary.mq.broker import broker


@broker.task
async def download_youtube_audio(
        temp_path: Path, url: str,
        from_time: Optional[str] = None, to_time: Optional[str] = None
) -> Path:
    req_dict: dict = YoutubeDL(
        params={"playlist_items": "1"}
    ).extract_info(url=url, download=False)

    if req_dict.get("entries") is not None:
        info_dict = req_dict["entries"][0]
    else:
        info_dict = req_dict

    url_duration = info_dict.get("duration")
    title = info_dict.get("title")
    channel = info_dict.get("channel")
    filename = f"{channel} - {title}" if title and channel else uuid.uuid4().hex

    filename_with_ext = filename + ".mp3"
    downloaded_file_path = temp_path / filename_with_ext

    ydl_opts: dict = {
        "extract_audio": True,
        "format": "bestaudio[ext=mp4]",
        "add_metadata": True,
        "embed_thumbnail": True,
        "metadata_from_title": "%(title)s",
        "parse_metadata": "title:%(artist)s - %(title)s",
        "outtmpl": downloaded_file_path.resolve().as_posix(),
        "external_downloader": "ffmpeg",
        "external_downloader_args": {"ffmpeg": ["-acodec", "libmp3lame"]}
    }
    if from_time and to_time:
        from_time = datetime.fromisoformat(from_time)
        to_time = datetime.fromisoformat(to_time)
        duration = (to_time - from_time).total_seconds()
    else:
        duration = url_duration
    if duration > 600:
        raise BigDurationError

    ffmpeg_options: list[str] = ydl_opts["external_downloader_args"]["ffmpeg"]
    if from_time:
        ffmpeg_options.extend(["-ss", from_time.strftime(r"%H:%M:%S")])
    if to_time:
        ffmpeg_options.extend(["-to", to_time.strftime(r"%H:%M:%S")])

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(info_dict["original_url"])

    return downloaded_file_path


@broker.task
async def process_thumbnail(image_path: Path) -> Path:
    quality = 1024
    with Image.open(image_path) as image:
        new_image = ImageOps.fit(
            image=image,
            size=(quality, quality)
        )
    new_image_filename = uuid.uuid4().hex
    new_image_path = image_path.parent / new_image_filename
    new_image.save(fp=new_image_path, format="jpeg")
    return new_image_path
