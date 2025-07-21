import asyncio

from aiogram import Bot, Dispatcher

def get_token():
    token = ''
    try:
        f = open('TG_TOKEN.txt', 'r')
        token = f.readline().strip()  # Укажите путь к chromedriver
        f.close()
    except Exception as e:
        print(e)
    return token
