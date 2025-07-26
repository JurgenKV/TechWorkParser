from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import WorkFilter
import TG_Bot.keyboards as kb
from TG_Bot.sender import send_works_in_chunks
from TG_Bot.utils import shorten_url

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    from TG_Bot.sender import TECH_LIST_PRIVATE
    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 1)
    filtered = WorkFilter.sort_by_nearest_work(filtered)
    if message.chat.type == "private":
        await send_works_in_chunks(message, filtered, "за сегодня")
        await message.answer("Выберите действие:", reply_markup=kb.main)
    else:
        await message.sender(f"Бот подключен в чате", reply_markup=None)

@router.message(F.text == 'За сегодня')
async def works_by_1(message: Message):
    from TG_Bot.sender import TECH_LIST_PRIVATE
    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 1)
    filtered = WorkFilter.sort_by_nearest_work(filtered)
    await send_works_in_chunks(message, filtered, "за сегодня")

@router.message(F.text == 'За 3 дня')
async def works_by_3(message: Message):
    from TG_Bot.sender import TECH_LIST_PRIVATE
    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 3)
    filtered = WorkFilter.sort_by_nearest_work(filtered)
    await send_works_in_chunks(message, filtered, "за 3 дня")


@router.message(F.text == 'За 7 дней')
async def works_by_7(message: Message):
    from TG_Bot.sender import TECH_LIST_PRIVATE
    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 7)
    filtered = WorkFilter.sort_by_nearest_work(filtered)
    await send_works_in_chunks(message, filtered, "за 7 дней")


@router.message(F.text == 'За 14 дней')
async def works_by_14(message: Message):
    from TG_Bot.sender import TECH_LIST_PRIVATE
    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 14)
    filtered = WorkFilter.sort_by_nearest_work(filtered)
    await send_works_in_chunks(message, filtered, "за 14 дней")

