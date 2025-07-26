import logging
from datetime import datetime

LOGGER = logging.getLogger("AppLogger")

def setup_logger(log_file: str):
    LOGGER.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    LOGGER.addHandler(file_handler)

def info(message: str):
    try:
        LOGGER.info(message)
    except Exception as e:
        print(e)

def warning(message: str):
    try:
        LOGGER.warning(message)
    except Exception as e:
        print(e)

def error(message: str):
    try:
        LOGGER.error(message)
    except Exception as e:
        print(e)
