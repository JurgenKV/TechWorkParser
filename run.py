import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

import Parsers
import WorkFilter
from TechData import TechData

from TG_Bot.handlers import router
from TG_Bot.handlers import update_tech_data_periodically


def get_token():
    token = ''
    try:
        f = open('TG_Bot\\TG_TOKEN.txt', 'r')
        token = f.readline().strip()
        f.close()
    except Exception as e:
        print(e)
    return str(token)

bot = Bot(token=get_token())
disp = Dispatcher(storage=MemoryStorage())

async def main():
    asyncio.create_task(update_tech_data_periodically())
    disp.include_routers(router)
    await disp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Run Error')


