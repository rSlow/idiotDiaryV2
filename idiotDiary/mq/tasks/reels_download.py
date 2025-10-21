from pathlib import Path

from instaloader import instaloader

from idiotDiary.mq.broker import broker
from idiotDiary.mq.utils.exceptions import NoReelDownloadedError


@broker.task
def download_instagram_reel(
        temp_folder: Path, reel_id: str,
) -> Path:
    loader = instaloader.Instaloader(
        save_metadata=False,
        download_video_thumbnails=False,
        filename_pattern="reel"
    )
    loader.download_post(
        post=instaloader.Post.from_shortcode(
            context=loader.context,
            shortcode=reel_id,
        ),
        target=temp_folder
    )

    reel_downloaded_file_path = temp_folder / "reel.mp4"
    if not reel_downloaded_file_path.is_file():
        raise NoReelDownloadedError

    return reel_downloaded_file_path
