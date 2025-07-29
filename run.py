import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import TG_Bot.config
from LOG import setup_logger

from TG_Bot.handlers import router
from TG_Bot.sender import update_tech_data_periodically
from TG_Bot.sender import send_shutdown_message
import LOG

bot = Bot(token=TG_Bot.config.get_token())
disp = Dispatcher(storage=MemoryStorage())

async def main():
    try:
        setup_logger()
        asyncio.create_task(update_tech_data_periodically())
        disp.include_router(router)
        await disp.start_polling(bot)
    except Exception as e:
        LOG.error(f"Критическая ошибка.: {str(e)}")
        raise
    finally:
        await send_shutdown_message()
        LOG.info("Бот успешно завершил работу.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Работа бота была прервана пользователем.')
        LOG.warning('Работа бота была прервана пользователем.')
    except Exception as e:
        print(f'Произошла ошибка: {str(e)}')
        LOG.error(f'Произошла ошибка: {str(e)}')