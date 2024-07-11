from pathlib import Path

from config.settings import ENV

APP_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = APP_DIR / "templates"
APP_TEMP_ROOT = APP_DIR / "temp"

MORPH_URL = ENV.str("MORPH_URL")
MORPH_CASE_ALIASES = {
    "1": "Именительный",
    "2": "Родительный",
    "3": "Дательный",
    "4": "Винительный",
    "5": "Творительный",
    "6": "Предложный",
}
SELENIUM_URL: str = ENV.str("SELENIUM_URL")

