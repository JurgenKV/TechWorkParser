import asyncio

from aiogram import Bot, Dispatcher
GROUP_CHAT_ID = '-4630597038' # empty test group
#TG_BOT_TOKEN = '8285879690:AAHLJevNMWGLien8u_PQkB3LGCO4dIWK1DU' #test bot
def get_token():
    token = ''
    try:
        f = open('TG_TOKEN.txt', 'r')
        token = f.readline().strip()
        f.close()
    except Exception as e:
        print(e)
    return token
