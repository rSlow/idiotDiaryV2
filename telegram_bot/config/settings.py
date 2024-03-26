from pathlib import Path

import pytz

from .env import get_env

BASE_DIR = Path(__file__).resolve().parent.parent

ENV = get_env(env_file=BASE_DIR / ".env")

DEBUG: bool = ENV.bool("DEBUG", None)

WEBHOOK_SECRET: str | None = ENV.str("WEBHOOK_SECRET", None)
WEBHOOK_PATH: str = ENV.str("WEBHOOK_PATH")
BASE_WEBHOOK_URL: str = ENV.str("BASE_WEBHOOK_URL")
BASE_WEBHOOK_PORT: str = ENV.str("BASE_WEBHOOK_PORT", "443")
WEB_SERVER_PORT: int = ENV.int("WEB_SERVER_PORT")

TIMEZONE = pytz.timezone(ENV.str("TIMEZONE", "Asia/Vladivostok"))
OWNER_ID: str = ENV.str("OWNER_ID")
BIRTHDAYS_ALLOWED: list[str] = ENV.list("BIRTHDAYS_ALLOWED", [])

LOGS_FOLDER = "logs"
LOGS_DIR = BASE_DIR / LOGS_FOLDER

REDIS_HOST: str = ENV.str("REDIS_HOST")
REDIS_PORT: int = ENV.int("REDIS_PORT")
REDIS_PASS: str = ENV.str("REDIS_PASS")
REDIS_DB: int = ENV.int("REDIS_DB")
REDIS_URL: str = ENV.str("REDIS_URL")
