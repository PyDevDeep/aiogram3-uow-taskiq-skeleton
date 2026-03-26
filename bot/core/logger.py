import logging
import os
from logging.handlers import RotatingFileHandler

from bot.core.config import settings


def configure_logging() -> None:
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_filename = f"{log_dir}/bot.log"

    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(log_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    noisy_loggers = {
        "urllib3": logging.WARNING,
        "httpcore": logging.INFO,
        "httpx": logging.INFO,
        "aiogram": logging.INFO,
        "taskiq": logging.WARNING,
    }

    for logger_name, level in noisy_loggers.items():
        logging.getLogger(logger_name).setLevel(level)
