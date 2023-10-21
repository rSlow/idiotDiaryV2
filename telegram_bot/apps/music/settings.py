from pathlib import Path

TEMP_DIR = Path(__file__).resolve().parent / "temp"
HTTPS_REGEXP = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
TIMECODE_REGEXP = r"(\d{2}:)?\d{2}:\d{2}"
FULL_TIMECODE_REGEXP = TIMECODE_REGEXP + r"-" + TIMECODE_REGEXP
AUDIO_FILE_EXT = ".mp3"
