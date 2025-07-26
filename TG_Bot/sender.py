import asyncio
import logging
from datetime import datetime, timedelta

from aiogram.types import Message

import Parsers
import WorkFilter
from TG_Bot import config
from TG_Bot.utils import shorten_url
from TechData import TechData
from TG_Bot.keyboards import main as kb
TECH_LIST_PRIVATE = []
TECH_LIST_TODAY = []

import LOG

async def send_new_works_to_group(new_works: list[TechData]):
    try:
        if not new_works:
            LOG.info("Новых работ нет.")
            return

        chunk_size = 10
        chunks = [new_works[i:i + chunk_size] for i in range(0, len(new_works), chunk_size)]

        from run import bot
        for i, chunk in enumerate(chunks, start=1):
            works_message = f"Технические работы (часть {i}/{len(chunks)}):\n\n"
            for new_work in chunk:
                works_message += (
                    f'<b><i>[{new_work.publishing_date}] {new_work.service_type}</i></b>\n'
                    f'<b>Заголовок:</b> {new_work.work_header}\n'
                    f'<b>Описание:</b> {new_work.description}\n'
                    f'<b>Дата проведения:</b> {new_work.date_of_work}\n'
                    f'<b>Ссылка:</b> {shorten_url(new_work.link)}\n\n'
                )
            try:
                await bot.send_message(chat_id=config.GROUP_CHAT_ID, text=works_message, parse_mode='HTML')
                LOG.info(f"Отправлен чанк {i}/{len(chunks)} с {len(chunk)} работами.")
            except Exception as e:
                LOG.error(f"Ошибка при отправке чанка {i}: {e}")
                break

        LOG.info(f"Всего отправлено {len(new_works)} новых работ в группу.")
    except Exception as e:
        LOG.error(f"Ошибка отправки данных в группу: {e}")

async def send_works_in_chunks(message: Message, works: list, period: str):
    chunk_size = 10
    chunks = [works[i:i + chunk_size] for i in range(0, len(works), chunk_size)]

    for i, chunk in enumerate(chunks, start=1):
        works_message = f"Технические работы <b>{period.lower()}</b> (часть {i}/{len(chunks)}):\n\n"
        for new_work in chunk:
            works_message += (f'<b><i>[{new_work.publishing_date}] {new_work.service_type}</i></b>\n'
                              f'<b>Заголовок:</b> {new_work.work_header}\n'
                              f'<b>Описание:</b> {new_work.description}\n'
                              f'<b>Дата проведения:</b> {new_work.date_of_work}\n'
                              f'<b>Ссылка:</b> {shorten_url(new_work.link)}\n\n')
        try:
            await message.answer(works_message,  parse_mode='HTML', markup=kb)
        except Exception as e:
            await message.answer(f"Ошибка при отправке сообщения: {e}")
            break


async def update_tech_data_periodically():
    global TECH_LIST_PRIVATE
    global TECH_LIST_TODAY
    # Инициализация начального списка работ
    initial_data = Parsers.get_all_parsing_data()
    LOG.info(f"Данные от парсера при инициализации: {initial_data}")

    TECH_LIST_PRIVATE = WorkFilter.get_works_by_period(initial_data, 14)
    TECH_LIST_PRIVATE = WorkFilter.sort_by_nearest_work(TECH_LIST_PRIVATE)

    TECH_LIST_TODAY = WorkFilter.get_works_by_period(initial_data, 1)
    TECH_LIST_TODAY = WorkFilter.sort_by_nearest_work(TECH_LIST_TODAY)
    await send_startup_message()
    await send_new_works_to_group(TECH_LIST_TODAY)
    LOG.info("Список технических работ успешно инициализирован.")

    while True:
        now = datetime.now()
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        sleep_time = (next_hour - now).total_seconds()

        await asyncio.sleep(sleep_time)  # Ждем до следующего часа
        initial_data = Parsers.get_all_parsing_data()
        TECH_LIST_PRIVATE = WorkFilter.get_works_by_period(initial_data, 14)
        TECH_LIST_PRIVATE = WorkFilter.sort_by_nearest_work(TECH_LIST_PRIVATE)

        try:
            # Получаем новый список работ
            new_tech_list = WorkFilter.get_works_by_period(initial_data, 1)
            new_tech_list = WorkFilter.sort_by_nearest_work(new_tech_list)

            # Проверяем, что списки не пустые
            if not new_tech_list:
                LOG.warning("Новый список работ пуст.")
                continue

            if not TECH_LIST_TODAY:
                LOG.warning("Текущий список работ пуст. Инициализирую заново.")
                TECH_LIST_TODAY = new_tech_list.copy()
                continue

            # Находим новые работы (по уникальному идентификатору)
            new_works = [
                work for work in new_tech_list
                if work.link and work.service_type and work.work_header not in [item.link and item.service_type and item.work_header for item in TECH_LIST_TODAY]
            ]

            # Отправляем новые работы в группу
            if new_works:
                await send_new_works_to_group(new_works)
                LOG.info(f"Отправлено {len(new_works)} новых работ.")
            else:
                LOG.info("Новых работ нет.")

            # Обновляем глобальный список
            TECH_LIST_TODAY = new_tech_list.copy()

        except Exception as e:
            LOG.error(f"Ошибка при обновлении данных: {e}")

async def send_shutdown_message():
    try:
        from run import bot
        text = "Бот отключен ⚠️"
        await bot.send_message(chat_id=config.GROUP_CHAT_ID, text=text, parse_mode='HTML')
    except Exception as e:
        LOG.error(f"Ошибка при отправке сообщения о выключении: {e}")

async def send_startup_message():
    try:
        from run import bot
        text = "Бот подключен ✅"
        await bot.send_message(chat_id=config.GROUP_CHAT_ID, text=text, parse_mode='HTML')
    except Exception as e:
        LOG.error(f"Ошибка при отправке сообщения о включении: {e}")