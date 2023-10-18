import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from contextlib import redirect_stdout
from io import BytesIO

from yt_dlp import YoutubeDL


def download_audio(url: str) -> BytesIO:
    ydl_opts = {
        'extract_audio': True,
        'format': 'bestaudio',
        # 'outtmpl': '123.mp3',
        'outtmpl': '-',
        'logger': logging.getLogger()
    }
    audio_io = BytesIO()
    with redirect_stdout(audio_io):
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    audio_io.seek(0)
    return audio_io
