import logging
import sys
from config import Config

def setup_logger(name: str = "FakeNewsIdentifier") -> logging.Logger:
    """Configures application logger with console and file handlers."""
    logger = logging.getLogger(name)
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Stream Handler (Console)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # File Handler
        try:
            file_handler = logging.FileHandler(Config.LOG_FILE, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not initialize file log handler: {e}")

    return logger

logger = setup_logger()
