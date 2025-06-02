import logging
import os
import sys
from logging.handlers import RotatingFileHandler


def setup_logger(name: str) -> logging.Logger:
    log_path = os.path.join(os.getcwd(), "logs", "app.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger  # Avoid adding handlers multiple times

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Stream handler (console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # File handler with rotation
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    file_handler = RotatingFileHandler(
        log_path, maxBytes=9000000, backupCount=3, delay=True
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
