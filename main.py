from typing import List
from pathlib import Path
from os import environ
from telethon import TelegramClient, events
from business_functions import *


class FUCK_USELF(Exception):
    pass


def update_env():
    try:
        with (Path(__file__).absolute().parent / '.env').open() as file:
            for name_val in map(lambda x: x.strip().split('='), file.readlines()):
                environ[name_val[0]] = name_val[1]
    except FileNotFoundError:
        raise FUCK_USELF('You should create the FUCKING .env FILE')


update_env()
bot = TelegramClient('bot', environ['API_ID'], environ['API_HASH']).start(bot_token=environ['BOT_TOKEN'])


@bot.on(events.ChatAction)
async def new_user(event: events.ChatAction):
    if event.user_joined:
        await new_user_worker(event, bot)


@bot.on(event=events.NewMessage)
async def some_message(event: events.NewMessage):
    await new_message_worker(event)


if __name__ == '__main__':
    bot.run_until_disconnected()
