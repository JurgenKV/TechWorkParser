import asyncio

from aiogram import Bot, Dispatcher

GROUP_CHAT_ID = '-1002717193981' # TEST чат sandbox
#TG_BOT_TOKEN = '8109684400:AAHUU5I51x_oWSiT6DHuJ9KBlWyr54fiFks' # тест бот sandbox

def get_token():
    token = ''
    try:
        f = open('TG_TOKEN.txt', 'r')
        token = f.readline().strip()  # Укажите путь к chromedriver
        f.close()
    except Exception as e:
        print(e)
    return token
