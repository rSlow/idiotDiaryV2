from datetime import time

from pydantic import BaseModel, AnyHttpUrl


class SYoutube(BaseModel):
    url: AnyHttpUrl
    from_time: time
    to_time: time
