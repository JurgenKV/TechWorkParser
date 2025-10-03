import asyncio
import logging
import traceback
from datetime import datetime, timedelta, time

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
            works_message = f"<b>Новые технические работы (часть {i}/{len(chunks)}):</b>\n\n"
            for new_work in chunk:
                works_message += (
                    f'<b><i>[{new_work.publishing_date}] {new_work.service_type}</i></b>\n'
                    f'<b>Заголовок:</b> {new_work.work_header}\n'
                    f'<b>Описание:</b> {new_work.description}\n'
                    f'<b>Дата проведения:</b> {new_work.date_of_work}\n'
                    f'<b>Ссылка:</b> {shorten_url(new_work.link)}\n\n'
                )
            try:
                works_message += f"<b>Новые технические работы (часть {i}/{len(chunks)})</b>\n"
                await bot.send_message(chat_id=config.GROUP_CHAT_ID, text=works_message, parse_mode='HTML',disable_web_page_preview=True)
                LOG.info(f"Отправлен чанк {i}/{len(chunks)} с {len(chunk)} работами.")
            except Exception as e:
                LOG.error(f"Ошибка при отправке чанка {i}: {e}")
                break

        LOG.info(f"Всего отправлено {len(new_works)} новых работ в группу.")
    except Exception as e:
        LOG.error(f"Ошибка отправки данных в группу: {e}")

async def send_summary_works_to_group(works: list[TechData]):
    try:
        if not works:
            LOG.info("Работ нет.")
            return

        chunk_size = 10
        chunks = [works[i:i + chunk_size] for i in range(0, len(works), chunk_size)]

        from run import bot
        for i, chunk in enumerate(chunks, start=1):
            works_message = f"<b>СВОДКА за 2 дня.\nТехнические работы (часть {i}/{len(chunks)}):</b>\n\n"
            for new_work in chunk:
                works_message += (
                    f'<b><i>[{new_work.publishing_date}] {new_work.service_type}</i></b>\n'
                    f'<b>Заголовок:</b> {new_work.work_header}\n'
                    f'<b>Описание:</b> {new_work.description}\n'
                    f'<b>Дата проведения:</b> {new_work.date_of_work}\n'
                    f'<b>Ссылка:</b> {shorten_url(new_work.link)}\n\n'
                )
            try:
                works_message += f"<b>СВОДКА за 2 дня.\nТехнические работы (часть {i}/{len(chunks)})</b>\n"
                await bot.send_message(chat_id=config.GROUP_CHAT_ID, text=works_message, parse_mode='HTML',disable_web_page_preview=True)
                LOG.info(f"Отправлен чанк {i}/{len(chunks)} с {len(chunk)} работами.")
            except Exception as e:
                LOG.error(f"Ошибка при отправке чанка {i}: {e}")
                break

        LOG.info(f"Всего отправлено {len(works)} сводных работ в группу.")
    except Exception as e:
        LOG.error(f"Ошибка отправки данных в группу: {e}")

async def send_works_in_chunks(message: Message, works: list, period: str):
    chunk_size = 10
    chunks = [works[i:i + chunk_size] for i in range(0, len(works), chunk_size)]

    for i, chunk in enumerate(chunks, start=1):
        works_message = f"<b>Технические работы <b>{period.lower()}</b> (часть {i}/{len(chunks)}):</b>\n\n"
        for new_work in chunk:
            works_message += (f'<b><i>[{new_work.publishing_date}] {new_work.service_type}</i></b>\n'
                              f'<b>Заголовок:</b> {new_work.work_header}\n'
                              f'<b>Описание:</b> {new_work.description}\n'
                              f'<b>Дата проведения:</b> {new_work.date_of_work}\n'
                              f'<b>Ссылка:</b> {shorten_url(new_work.link)}\n\n')
        try:
            works_message += f"Технические работы <b>{period.lower()}</b> (часть {i}/{len(chunks)})"
            await message.answer(works_message,  parse_mode='HTML', markup=kb,disable_web_page_preview=True)
        except Exception as e:
            await message.answer(f"Ошибка при отправке сообщения: {e}")
            break

async def send_works_in_chunks_only_service(message: Message, works: list, period: str):
    chunk_size = 100
    chunks = [works[i:i + chunk_size] for i in range(0, len(works), chunk_size)]

    for i, chunk in enumerate(chunks, start=1):
        works_message = f"Технические работы поставщиков <b>{period.lower()}</b> (часть {i}/{len(chunks)}):\n\n"
        for new_work in chunk:
            works_message += (
                f'<b><i>[{new_work.publishing_date}] <a href="{new_work.link}">{new_work.service_type}</a></i></b>\n'
            )
        try:
            works_message += f"\nТехнические работы поставщиков <b>{period.lower()}</b> (часть {i}/{len(chunks)}):\n"
            await message.answer(works_message,  parse_mode='HTML', markup=kb,disable_web_page_preview=True)
        except Exception as e:
            await message.answer(f"Ошибка при отправке сообщения: {e}")
            break


async def update_tech_data_periodically():
    global TECH_LIST_PRIVATE
    global TECH_LIST_TODAY

    def is_valid_work_list(work_list):
        return all(
            hasattr(work, 'link') and
            hasattr(work, 'service_type') and
            hasattr(work, 'work_header') and
            work.link and work.service_type and work.work_header
            for work in work_list
        )

    try:
        initial_data = Parsers.get_all_parsing_data()
        LOG.info(f"Данные от парсера при инициализации: {initial_data}")

        TECH_LIST_PRIVATE = WorkFilter.get_works_by_period(initial_data, 14)
        TECH_LIST_PRIVATE = WorkFilter.sort_by_nearest_work(TECH_LIST_PRIVATE)

        TECH_LIST_TODAY = WorkFilter.get_works_by_period(initial_data, 1)
        TECH_LIST_TODAY = WorkFilter.sort_by_nearest_work(TECH_LIST_TODAY)

        await send_startup_message()
        await send_new_works_to_group(TECH_LIST_TODAY)
        LOG.info("Список технических работ успешно инициализирован.")

    except Exception as e:
        LOG.error(f"Ошибка при инициализации данных: {e}\n{traceback.format_exc()}")
        LOG.info("Перезапуск инициализации через 1 минуту...")
        await asyncio.sleep(60)
        await update_tech_data_periodically()
        return

    while True:
        try:
            now = datetime.now()
            next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            sleep_time = (next_hour - now).total_seconds()
            await asyncio.sleep(sleep_time)

            initial_data = Parsers.get_all_parsing_data()
            TECH_LIST_PRIVATE = WorkFilter.get_works_by_period(initial_data, 14)
            TECH_LIST_PRIVATE = WorkFilter.sort_by_nearest_work(TECH_LIST_PRIVATE)

            new_tech_list = WorkFilter.get_works_by_period(initial_data, 1)
            new_tech_list = WorkFilter.sort_by_nearest_work(new_tech_list)

            if not new_tech_list or not is_valid_work_list(new_tech_list):
                LOG.warning("Новый список работ пуст или содержит некорректные данные.")
                continue

            if not TECH_LIST_TODAY or not is_valid_work_list(TECH_LIST_TODAY):
                LOG.warning("Текущий список работ пуст или содержит некорректные данные. Инициализирую заново.")
                TECH_LIST_TODAY = new_tech_list.copy()
                continue

            current_ids = {(item.link, item.service_type, item.work_header) for item in TECH_LIST_TODAY}
            new_works = [
                work for work in new_tech_list
                if (work.link, work.service_type, work.work_header) not in current_ids
            ]

            if new_works:
                try:
                    await send_new_works_to_group(new_works)
                    LOG.info(f"Отправлено {len(new_works)} новых работ.")
                except Exception as e:
                    LOG.error(f"Ошибка при отправке новых работ: {e}\n{traceback.format_exc()}")
            else:
                LOG.info("Новых работ нет.")

            TECH_LIST_TODAY = new_tech_list.copy()

        except Exception as e:
            LOG.error(f"Критическая ошибка в основном цикле: {e}\n{traceback.format_exc()}")
            LOG.info("Перезапуск цикла через 1 минуту...")
            await asyncio.sleep(60)

async def send_shutdown_message():
    try:
        from run import bot
        text = "Бот отключен ⚠️"
        await bot.send_message(chat_id=config.GROUP_CHAT_ID, text=text, parse_mode='HTML',disable_web_page_preview=True)
    except Exception as e:
        LOG.error(f"Ошибка при отправке сообщения о выключении: {e}")

async def send_startup_message():
    try:
        from run import bot
        text = "Бот подключен ✅"
        await bot.send_message(chat_id=config.GROUP_CHAT_ID, text=text, parse_mode='HTML',disable_web_page_preview=True)
    except Exception as e:
        LOG.error(f"Ошибка при отправке сообщения о включении: {e}")

async def send_summary_works():
    try:
        # Таргет времени: 20:50 и 8:50
        target_time_1 = time(20, 50)
        target_time_2 = time(8, 50)

        while True:
            now = datetime.now().time()

            # Проверяем, какое из времён наступит раньше
            if now < target_time_1 and now < target_time_2:
                # Если текущее время раньше обоих целевых времён, выбираем ближайшее
                next_time = min(target_time_1, target_time_2)
            elif now < target_time_1:
                next_time = target_time_1
            else:
                # Если текущее время позже 21:10, следующее время — 9:10
                next_time = target_time_2

            now_dt = datetime.now()  # Полная дата и время
            next_dt = datetime.combine(now_dt.date(), next_time)
            if now_dt.time() > next_time:
                next_dt += timedelta(days=1)

            sleep_time = (next_dt - now_dt).total_seconds()

            await asyncio.sleep(sleep_time)

            try:
                filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 2)
                filtered = WorkFilter.sort_by_nearest_work(filtered)
                if filtered:
                    try:
                        await send_summary_works_to_group(filtered)
                        LOG.info(f"Отправлена {len(filtered)} сводка  работ.")
                    except Exception as e:
                        LOG.error(f"Ошибка при отправке сводных работ: {e}\n{traceback.format_exc()}")
            except Exception as send_error:
                print(f"Ошибка при отправке сообщения: {send_error}")
                LOG.error(f"Ошибка при отправке сообщения: {send_error}")

            sleep_duration = timedelta(hours=11, minutes=50).total_seconds()
            await asyncio.sleep(sleep_duration)

    except Exception as e:
        print("Ошибка в функции отправки сводки по тех. работам")
        LOG.error(f"Ошибка в функции отправки сводки по тех. работам: {e}")

async def admin_send_summary_works():
    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 2)
    filtered = WorkFilter.sort_by_nearest_work(filtered)
    if filtered:
        try:
            await send_summary_works_to_group(filtered)
            LOG.info(f"Admin. Отправлена {len(filtered)} сводка  работ.")
        except Exception as e:
            LOG.error(f"Admin. Ошибка при отправке сводных работ: {e}\n{traceback.format_exc()}")