from pathlib import Path

import pytz

from .env import get_env

BASE_DIR = Path(__file__).resolve().parent.parent

ENV = get_env(env_file=BASE_DIR / ".env")
TEMPLATES_DIR = BASE_DIR / "common" / "jinja"

SECRET_HEADER = "X-Telegram-Bot-Api-Secret-Token"

WEBHOOK_SECRET = ENV.str("WEBHOOK_SECRET")
WEBHOOK_PATH = ENV.str("WEBHOOK_PATH")
BASE_WEBHOOK_URL = ENV.str("BASE_WEBHOOK_URL")
WEB_SERVER_HOST = ENV.str("WEB_SERVER_HOST")
WEB_SERVER_PORT = ENV.int("WEB_SERVER_PORT")

MORPH_URL = ENV.str("MORPH_URL")
MORPH_CASE_ALIASES = {
    "1": "Именительный",
    "2": "Родительный",
    "3": "Дательный",
    "4": "Винительный",
    "5": "Творительный",
    "6": "Предложный",
}

TIMEZONE = pytz.timezone(ENV.str("TIMEZONE"))
OWNER_ID = ENV.str("OWNER_ID")
SELENIUM_PORT = ENV.int("SELENIUM_PORT")

LOGS_FOLDER = "logs"
LOGS_DIR = BASE_DIR / LOGS_FOLDER
