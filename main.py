from typing import List
from pathlib import Path
from os import environ
from telethon import TelegramClient, events
from business_functions import *
import logging

logging.basicConfig(level=logging.INFO)


class EnvFileNotFoundError(Exception):
    pass


def update_env():
    try:
        with (Path(__file__).absolute().parent / '.env').open() as file:
            for name_val in map(lambda x: x.strip().split('='), file.readlines()):
                environ[name_val[0]] = name_val[1]
    except FileNotFoundError:
        raise EnvFileNotFoundError('You should create the FUCKING .env FILE')


update_env()
bot = TelegramClient('bot', environ['API_ID'], environ['API_HASH']).start(bot_token=environ['BOT_TOKEN'])


@bot.on(events.ChatAction)
async def new_user(event: events.ChatAction):
    if event.user_joined:
        logging.debug(
            f'{event.user.first_name} {event.user.last_name} https://t.me/{event.user.username} joined the chat {event.chat.title}')
        if not event.chat.admin_rights.ban_users:
            logging.debug(f'the bot has no rights to moderate {event.chat.title}')
            return
        await new_user_worker(event, bot)


@bot.on(events.NewMessage)
async def some_message(event: events.NewMessage):
    if event.text.startswith('/start') and event.is_private:
        await start_msg(event)
    else:
        await new_message_worker(event, bot)


if __name__ == '__main__':
    bot.run_until_disconnected()
