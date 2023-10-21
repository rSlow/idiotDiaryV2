import logging
import os
import sys

from loguru import logger

from config import settings
from config.settings import ENV

LOGS_FOLDER = "logs"
LOGS_DIR = settings.BASE_DIR / LOGS_FOLDER


def init_logging():
    if not LOGS_DIR.is_dir():
        os.mkdir(LOGS_FOLDER)

    logging.basicConfig(
        level=logging.INFO,
        filename=LOGS_DIR / "log.log",
        format="[%(asctime)s - %(levelname)s] %(name)s - %(message)s",
    )


logger.remove()
loguru_sink = ENV.str("LOGURU_FILE", None)
logger.add(
    sink=LOGS_DIR / loguru_sink if loguru_sink is not None else sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
    colorize=bool(loguru_sink)
)
