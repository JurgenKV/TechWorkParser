import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

import Parsers
import WorkFilter
from LOG import setup_logger
from TechData import TechData

from TG_Bot.handlers import router
from TG_Bot.sender import update_tech_data_periodically
from TG_Bot.sender import send_shutdown_message
from TG_Bot.sender import send_startup_message
import LOG

def get_token():
    token = ''
    try:
        f = open('TG_Bot\\TG_TOKEN.txt', 'r')
        token = f.readline().strip()
        f.close()
    except Exception as e:
        LOG.error(str(e))
    return str(token)

bot = Bot(token=get_token())
disp = Dispatcher(storage=MemoryStorage())

async def main():
    try:
        setup_logger("log.txt")
        asyncio.create_task(update_tech_data_periodically())
        disp.include_routers(router)
        await disp.start_polling(bot)
    finally:
        await send_shutdown_message()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Run Error')
        LOG.error('Run Error')


