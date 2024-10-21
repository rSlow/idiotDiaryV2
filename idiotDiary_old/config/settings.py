import os
from pathlib import Path

import pytz

from .enums import BotMode
from .env import get_env

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE: str = os.getenv("ENV_FILE", ".env")
ENV = get_env(env_file=BASE_DIR / ENV_FILE)

BOT_TOKEN = ENV.str("BOT_TOKEN")
DEBUG: bool = ENV.bool("DEBUG", False)
BOT_MODE: str = ENV.enum("BOT_MODE", BotMode.POOLING.value, type=BotMode)

WEBHOOK_SECRET: str | None = ENV.str("WEBHOOK_SECRET", None)
WEBHOOK_PATH: str = ENV.str("WEBHOOK_PATH")
WEBHOOK_ADDRESS: str = ENV.str("WEBHOOK_ADDRESS")
WEB_SERVER_PORT: int = ENV.int("WEB_SERVER_PORT")

TIMEZONE = pytz.timezone(ENV.str("TIMEZONE", "Asia/Vladivostok"))
OWNER_ID: str = ENV.str("OWNER_ID")
BIRTHDAYS_ALLOWED: list[str] = ENV.list("BIRTHDAYS_ALLOWED", [])

LOGS_FOLDER = "logs"
LOGS_DIR = BASE_DIR / LOGS_FOLDER

DATABASE_URL: str = ENV.str("DATABASE_URL")
REDIS_URL: str = ENV.str("REDIS_URL")
