import logging
from logging.handlers import TimedRotatingFileHandler
import os


def setup_logger(log_folder):
    os.makedirs(log_folder, exist_ok=True)

    log_file_format = os.path.join(log_folder, "application.log")
    logging.basicConfig(
        handlers=[TimedRotatingFileHandler(log_file_format, when="MIDNIGHT", interval=1, backupCount=3)],
        level=logging.INFO,
        format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] - %(message)s'
    )
    logger = logging.getLogger(__name__)

    return logger
