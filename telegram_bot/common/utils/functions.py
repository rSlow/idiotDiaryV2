from datetime import datetime
from config import settings


def get_now():
    return datetime.now().astimezone(tz=settings.TIMEZONE)
