import logging
import os
import sys
from config import Config

def setup_logger(name: str = "FakeNewsIdentifier") -> logging.Logger:
    """Configures application logger writing to logs/app.log and console."""
    logger = logging.getLogger(name)
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 1. Console Stream Handler
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # 2. File Handler (logs/app.log)
        try:
            os.makedirs(Config.LOGS_DIR, exist_ok=True)
            file_handler = logging.FileHandler(Config.LOG_FILE_PATH, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not initialize file log handler at {Config.LOG_FILE_PATH}: {e}")

    return logger

logger = setup_logger()
