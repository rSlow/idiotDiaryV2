import logging
import os
import sys

from loguru import logger

from config import settings


def init_logging() -> None:
    if not settings.LOGS_DIR.is_dir():
        os.mkdir(settings.LOGS_FOLDER)

    # ----- LOGGING -----
    logging.basicConfig(
        level=logging.INFO,
        filename=settings.LOGS_DIR / "log.log" if not settings.DEBUG else None,
        format="[%(asctime)s - %(levelname)s] %(name)s - %(message)s",
    )

    # ----- LOGURU -----
    logger.remove()
    logger.add(
        sink=settings.LOGS_DIR / "errors.log" if not settings.DEBUG else sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
        colorize=settings.DEBUG
    )
