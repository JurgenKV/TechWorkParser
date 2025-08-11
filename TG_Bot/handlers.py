import os
import shutil

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
import zipfile
import WorkFilter
import TG_Bot.keyboards as kb
#from TG_Bot.config import ADMIN_ID
from TG_Bot.sender import send_works_in_chunks, send_works_in_chunks_only_service
from TG_Bot.utils import shorten_url
from LOG import LOG_DIR
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

@router.message(F.text == 'За 2 дня')
async def works_by_3(message: Message):
    from TG_Bot.sender import TECH_LIST_PRIVATE
    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 2)
    filtered = WorkFilter.sort_by_nearest_work(filtered)
    await send_works_in_chunks(message, filtered, "за 2 дня")

@router.message(F.text == 'Поставщики за 3 дня')
async def works_by_14(message: Message):
    from TG_Bot.sender import TECH_LIST_PRIVATE
    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 3)
    filtered = WorkFilter.sort_by_nearest_work(filtered)
    await send_works_in_chunks_only_service(message, filtered, "за 3 дня (Поставщики)")

@router.message(F.text == 'За 3 дня')
async def works_by_3(message: Message):
    from TG_Bot.sender import TECH_LIST_PRIVATE
    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 3)
    filtered = WorkFilter.sort_by_nearest_work(filtered)
    await send_works_in_chunks(message, filtered, "за 3 дня")


@router.message(F.text == 'За 5 дней')
async def works_by_7(message: Message):
    from TG_Bot.sender import TECH_LIST_PRIVATE
    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 5)
    filtered = WorkFilter.sort_by_nearest_work(filtered)
    await send_works_in_chunks(message, filtered, "за 5 дней")


@router.message(F.text == 'За 14 дней')
async def works_by_14(message: Message):
    from TG_Bot.sender import TECH_LIST_PRIVATE
    filtered = WorkFilter.get_works_by_period(TECH_LIST_PRIVATE, 14)
    filtered = WorkFilter.sort_by_nearest_work(filtered)
    await send_works_in_chunks(message, filtered, "за 14 дней")

def create_logs_archive(log_directory, archive_name="logs.zip"):
    with zipfile.ZipFile(archive_name, 'w') as zipf:
        for root, _, files in os.walk(log_directory):
            for file in files:
                zipf.write(os.path.join(root, file), file)
    return archive_name


@router.message(F.text == '/get_logs')
async def cmd_get_logs(message: Message):
    # if message.from_user.id != ADMIN_ID:
    #     await message.answer("У вас нет прав для выполнения этой команды.")
    #     return
        # Проверяем, существует ли папка logs и содержит ли она файлы
    if not os.path.exists(LOG_DIR) or not os.listdir(LOG_DIR):
        await message.answer("Логи отсутствуют.")
        return
        # Получаем список всех файлов логов
    log_files = [f for f in os.listdir(LOG_DIR) if os.path.isfile(os.path.join(LOG_DIR, f))]

    if not log_files:
        await message.answer("Логи отсутствуют.")
        return
    try:
        for log_file in log_files:
            log_file_path = os.path.join(LOG_DIR, log_file)

            # Отправляем файл как документ
            document = FSInputFile(log_file_path, filename=log_file)
            await message.answer_document(document=document, caption=f"Лог-файл: {log_file}")

        await message.answer("Все файлы логов отправлены.")
    except Exception as e:
        await message.answer(f"Произошла ошибка при отправке логов: {str(e)}")


@router.message(F.text == '/delete_logs')
async def cmd_delete_logs(message: Message):
    # if message.from_user.id != ADMIN_ID:
    #     await message.answer("У вас нет прав для выполнения этой команды.")
    #     return

    if not os.path.exists(LOG_DIR) or not os.listdir(LOG_DIR):
        await message.answer("Логи отсутствуют.")
        return
    # Удаляем логи
    try:
        for filename in os.listdir(LOG_DIR):
            file_path = os.path.join(LOG_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        await message.answer("Все файлы логов успешно удалены.")
    except Exception as e:
        await message.answer(f"Произошла ошибка при удалении логов: {str(e)}")