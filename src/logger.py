# 📦 Module imports
import logging
from pathlib import Path

LOG_FILE = Path("logs/skycore.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Function: setup_logger — handles a core step in this module
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

# Function: log — handles a core step in this module
def log(message, level="info"):
    logger = logging.getLogger()
    if level == "info":
        logger.info(message)
    elif level == "error":
        logger.error(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "debug":
        logger.debug(message)
    else:
        logger.info(message)