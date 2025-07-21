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

router = Router()
TECH_LIST = []



def shorten_url(url):
    try:
        shortener = pyshorteners.Shortener()

        short_url = shortener.tinyurl.short(url)
        return short_url
    except Exception as e:
        print(f"Ошибка при сокращении ссылки: {e}")
        return url

@router.message(CommandStart())
async def cmd_start(message: Message):
    works_message = ''

    filtered = WorkFilter.get_works_by_period(TECH_LIST, 5)
    filtered = WorkFilter.sort_by_nearest_work(filtered)

    for notif in filtered:
        print(f"{notif.publishing_date} Сервис: {notif.service_type} = {notif.work_header} = {notif.link}")

    for notif in filtered:
        works_message += (f'[{notif.publishing_date}] {notif.service_type}\n'
                          f'{notif.work_header}\n'
                          f'{shorten_url(notif.link)}\n')

    await message.answer('Список Технических работ за 5 дней:\n'
                         f'{works_message}', reply_markup=kb.main)


async def update_tech_data_periodically():
    global TECH_LIST
    TECH_LIST = WorkFilter.get_works_by_period(Parsers.get_all_parsing_data(), 14)
    TECH_LIST = WorkFilter.sort_by_nearest_work(TECH_LIST)
    logging.info("Список технических работ успешно обновлен " + str(datetime.now().time()))

    while True:
        now = datetime.now()
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        sleep_time = (next_hour - now).total_seconds()

        await asyncio.sleep(sleep_time)
        try:
            TECH_LIST = WorkFilter.get_works_by_period(Parsers.get_all_parsing_data(), 14)
            TECH_LIST = WorkFilter.sort_by_nearest_work(TECH_LIST)
            logging.info("Список технических работ успешно обновлен.")
        except Exception as e:
            logging.error(f"Ошибка при обновлении данных: {e}")

@router.message(F.text=='За сегодня')
async def works_by_1(message: Message):
    works_message = ''

    filtered = WorkFilter.get_works_by_period(TECH_LIST, 1)
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

    filtered = WorkFilter.get_works_by_period(TECH_LIST, 3)
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

    filtered = WorkFilter.get_works_by_period(TECH_LIST, 5)
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

    filtered = WorkFilter.get_works_by_period(TECH_LIST, 7)
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