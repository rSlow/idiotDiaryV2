from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = APP_DIR / "templates"
TEMP_DIR = APP_DIR / "temp"
SINGLE_TIMECODE_REGEXP = r"^(\d{2}:)?\d{2}:\d{2}$"
PAIR_TIMECODE_REGEXP = SINGLE_TIMECODE_REGEXP[:-1] + r"-" + SINGLE_TIMECODE_REGEXP[1:]
AUDIO_FILE_EXT = ".mp3"
STRFTIME_FORMAT = "%H:%M:%S"
