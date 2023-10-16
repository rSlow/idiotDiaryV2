import logging
import os

from config import settings


def init_logging():
    logs_folder = "logs"
    if not (settings.BASE_DIR / logs_folder).is_dir():
        os.mkdir(logs_folder)

    logging.basicConfig(
        level=logging.INFO,
        filename=settings.BASE_DIR / logs_folder / "log.log",
        format="[%(asctime)s - %(levelname)s] %(name)s - %(message)s",
    )
