import logging
from contextlib import redirect_stdout
from io import BytesIO

from yt_dlp import YoutubeDL


def download_audio(url: str):
    ydl_opts = {
        'extract_audio': True,
        'format': 'bestaudio[ext=mp4]',
        'outtmpl': '-',
        'logger': logging.getLogger()
    }
    filename = "123.mp3"
    audio_io = BytesIO()
    with redirect_stdout(audio_io):
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    audio_io.seek(0)
    audio_bytes = audio_io.read()
    return audio_bytes, filename
