import logging
import os

from loguru import logger

from config import settings

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
logger.add(
    sink=LOGS_DIR / "errors.log",
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
)
