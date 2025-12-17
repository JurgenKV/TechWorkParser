import asyncio
from aiogram import Bot, Dispatcher
import os

CONFIG_FILE = "app_config.cfg"
DEFAULT_CONFIG = """GROUP_CHAT_ID:Replace by tg chat id
TG_TOKEN:Replace by tg token
CHROMEDRIVER_PATH:Replace by path to chromedriver
"""

def _ensure_config_exists():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(DEFAULT_CONFIG.strip() + "\n")
        print(f"Файл конфигурации не найден. Создан шаблон: {CONFIG_FILE}")


def _read_config_value(key: str) -> str:
    _ensure_config_exists()

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    if k.strip() == key:
                        return v.strip()

    raise KeyError(f"Ключ '{key}' не найден в {CONFIG_FILE}")


def get_group_chat_id() -> str:
    return _read_config_value("GROUP_CHAT_ID")


def get_tg_token() -> str:
    return _read_config_value("TG_TOKEN")


def get_chromedriver_path() -> str:
    return _read_config_value("CHROMEDRIVER_PATH")