import asyncio
import logging
from datetime import datetime, timedelta
import pyshorteners

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import Parsers
import WorkFilter
import TG_Bot.keyboards as kb
from TechData import TechData
import TG_Bot.config as config
router = Router()
TECH_LIST_PRIVATE = []
TECH_LIST_TODAY = []

def shorten_url(url):
    try:
        shortener = pyshorteners.Shortener()

        short_url = shortener.tinyurl.short(url)
        return short_url
    except Exception as e:
        print(f"Ошибка при сокращении ссылки: {e}")
        return url

async def send_new_works_to_group(new_works: list[TechData]):
    try:
        if not new_works:
            logging.info("Новых работ нет.")
            return
        works_message = ''
        for new_work in new_works:
            works_message += (f'[{new_work.publishing_date}] {new_work.service_type}\n'
                              f'{new_work.work_header}\n'
                              f'{shorten_url(new_work.link)}\n')
        from run import bot
        if works_message != '':
            await bot.send_message(chat_id=config.GROUP_CHAT_ID, text=works_message )
            logging.info(f"Отправлено {len(new_works)} новых работ в группу.")
        else:
            return
    except Exception as e:
        print('Ошибка отправки данных в группу' + str(e))

@router.message(CommandStart())
async def cmd_start(message: Message):
    works_message = ''

    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 5)
    filtered = WorkFilter.sort_by_nearest_work(filtered)

    for notif in filtered:
        print(f"{notif.publishing_date} Сервис: {notif.service_type} = {notif.work_header} = {notif.link}")

    for notif in filtered:
        works_message += (f'[{notif.publishing_date}] {notif.service_type}\n'
                          f'{notif.work_header}\n'
                          f'{shorten_url(notif.link)}\n')
    if message.chat.type == "private":
        await message.answer('Список Технических работ за 5 дней:\n'
                         f'{works_message}', reply_markup=kb.main)
    else:
        await message.answer(f'Бот подключен в чат:{message.chat.id}', reply_markup=None)

async def update_tech_data_periodically():
    global TECH_LIST_PRIVATE
    global TECH_LIST_TODAY

    # Инициализация начального списка работ
    initial_data = Parsers.get_all_parsing_data()
    logging.info(f"Данные от парсера при инициализации: {initial_data}")

    TECH_LIST_PRIVATE = WorkFilter.get_works_by_period(initial_data, 14)
    TECH_LIST_PRIVATE = WorkFilter.sort_by_nearest_work(TECH_LIST_PRIVATE)

    TECH_LIST_TODAY = WorkFilter.get_works_by_period(initial_data, 1)
    TECH_LIST_TODAY = WorkFilter.sort_by_nearest_work(TECH_LIST_TODAY)

    await send_new_works_to_group(TECH_LIST_TODAY)
    logging.info("Список технических работ успешно инициализирован.")

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
                logging.warning("Новый список работ пуст.")
                continue

            if not TECH_LIST_TODAY:
                logging.warning("Текущий список работ пуст. Инициализирую заново.")
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
                logging.info(f"Отправлено {len(new_works)} новых работ.")
            else:
                logging.info("Новых работ нет.")

            # Обновляем глобальный список
            TECH_LIST_TODAY = new_tech_list.copy()

        except Exception as e:
            logging.error(f"Ошибка при обновлении данных: {e}")

@router.message(F.text=='За сегодня')
async def works_by_1(message: Message):
    works_message = ''

    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 1)
    filtered = WorkFilter.sort_by_nearest_work(filtered)

    for notif in filtered:
        print(f"{notif.publishing_date} Сервис: {notif.service_type} = {notif.work_header} = {notif.link}")

    for notif in filtered:
        works_message += (f'[{notif.publishing_date}] {notif.service_type}\n'
                          f'{notif.work_header}\n'
                          f'{shorten_url(notif.link)}\n')
    try:
        await message.answer('Список Технических работ за сегодня:\n'
                         f'{works_message}')
    except Exception as e:
        await message.answer(str(e))

@router.message(F.text == 'За 3 дня')
async def works_by_3(message: Message):
    works_message = ''

    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 3)
    filtered = WorkFilter.sort_by_nearest_work(filtered)

    for notif in filtered:
        print(f"{notif.publishing_date} Сервис: {notif.service_type} = {notif.work_header} = {notif.link}")

    for notif in filtered:
        works_message += (f'[{notif.publishing_date}] {notif.service_type}\n'
                          f'{notif.work_header}\n'
                          f'{shorten_url(notif.link)}\n')
    try:
        await message.answer('Список Технических работ за 3 дня:\n'
                         f'{works_message}')
    except Exception as e:
        await message.answer(str(e))

@router.message(F.text=='За 5 дней')
async def works_by_7(message: Message):
    works_message = ''

    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 5)
    filtered = WorkFilter.sort_by_nearest_work(filtered)

    for notif in filtered:
        print(f"{notif.publishing_date} Сервис: {notif.service_type} = {notif.work_header} = {notif.link}")

    for notif in filtered:
        works_message += (f'[{notif.publishing_date}] {notif.service_type}\n'
                          f'{notif.work_header}\n'
                          f'{shorten_url(notif.link)}\n')

    try:
        await message.answer('Список Технических работ за 5 дней:\n'
                         f'{works_message}')
    except Exception as e:
        await message.answer(str(e))

@router.message(F.text=='За 7 дней')
async def works_by_14(message: Message):
    works_message = ''

    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 7)
    filtered = WorkFilter.sort_by_nearest_work(filtered)

    for notif in filtered:
        print(f"[{notif.publishing_date}] Сервис: {notif.service_type} = {notif.work_header} = {notif.link}")

    for notif in filtered:
        works_message += (f'[{notif.publishing_date}] {notif.service_type}\n'
                          f'{notif.work_header}\n'
                          f'{shorten_url(notif.link)}\n')
    try:
        await message.answer('Список Технических работ за 7 дней:\n'
                         f'{works_message}')
    except Exception as e:
        await message.answer(str(e))