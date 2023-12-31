from pathlib import Path

import pytz

from .env import get_env

BASE_DIR = Path(__file__).resolve().parent.parent

ENV = get_env(env_file=BASE_DIR / ".env")
TEMPLATES_DIR = BASE_DIR / "common" / "jinja"

WEBHOOK_SECRET = ENV.str("WEBHOOK_SECRET", None)
WEBHOOK_PATH = ENV.str("WEBHOOK_PATH")
BASE_WEBHOOK_URL = ENV.str("BASE_WEBHOOK_URL")
BASE_WEBHOOK_PORT = ENV.str("BASE_WEBHOOK_PORT", "443")
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

TIMEZONE = pytz.timezone(ENV.str("TIMEZONE", "Asia/Vladivostok"))
OWNER_ID = ENV.str("OWNER_ID")
SELENIUM_URL = ENV.str("SELENIUM_URL")

LOGS_FOLDER = "logs"
LOGS_DIR = BASE_DIR / LOGS_FOLDER
