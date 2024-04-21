from pathlib import Path
from environs import Env

ENV = Env()
BASE_DIR = Path(__file__).parent
TIME_FORMAT = "%H:%M:%S"
DEBUG = ENV.bool("YOUTUBE_DEBUG", False)
