from pathlib import Path

from .env import get_env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_DIR = BASE_DIR / "env"
ENV = get_env(env_dir=ENV_DIR)

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
