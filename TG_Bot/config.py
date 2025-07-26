import asyncio

from aiogram import Bot, Dispatcher

GROUP_CHAT_ID = '-1002687229910'
TG_BOT_TOKEN = 'ADD_TOken'
def get_token():
    token = ''
    try:
        f = open('TG_TOKEN.txt', 'r')
        token = f.readline().strip()  # Укажите путь к chromedriver
        f.close()
    except Exception as e:
        print(e)
    return token
