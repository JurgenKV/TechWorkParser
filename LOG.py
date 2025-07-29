import logging
from datetime import datetime
import os
LOG_DIR = 'logs'
# Создаем логгер
LOGGER = logging.getLogger("AppLogger")

def setup_logger():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_filename = f"logs_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    log_file_path = os.path.join(LOG_DIR, log_filename)

    LOGGER.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    LOGGER.addHandler(file_handler)

def info(message: str):
    try:
        LOGGER.info(message)
    except Exception as e:
        print(f"Ошибка при логировании INFO: {e}")

def warning(message: str):
    try:
        LOGGER.warning(message)
    except Exception as e:
        print(f"Ошибка при логировании WARNING: {e}")

def error(message: str):
    try:
        LOGGER.error(message)
    except Exception as e:
        print(f"Ошибка при логировании ERROR: {e}")