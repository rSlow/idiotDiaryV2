from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Request, HTTPException, status, Response, Body

import settings
from download import download
from exceptions import BigDurationError
import tempfile

from schemas import SYoutube

app = FastAPI(
    redoc_url=None,
    docs_url="/docs" if settings.DEBUG else None,
    debug=settings.DEBUG
)


@app.get("/")
async def test():
    return {"detail": "ok"}


@app.post("/download")
async def download_youtube_audio(data: Annotated[SYoutube, Body()]):
    string_url = str(data.url)

    with tempfile.TemporaryDirectory(dir=settings.BASE_DIR) as temp_dir:
        temp_path = Path(temp_dir)
        file_path = await download(
            url=string_url,
            dir_path=temp_path,
            from_time=data.from_time,
            to_time=data.to_time
        )
        with open(file_path, "rb") as file:
            file_data = file.read()
        return Response(
            content=file_data,
            media_type="audio/mp3"
        )


@app.exception_handler(BigDurationError)
async def big_duration_handler(_: Request,
                               exc: BigDurationError):
    raise HTTPException(
        status_code=status.HTTP_414_REQUEST_URI_TOO_LONG,
        detail=exc.args[0]
    )
