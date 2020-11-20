from typing import List
from pathlib import Path
from os import environ
from telethon import TelegramClient, events


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
clinet = TelegramClient('bot', environ['API_ID'], environ['API_HASH']).start(bot_token=environ['BOT_TOKEN'])


def find_FUCKING_words(text: str, blacklist: List[str] = ['блять', 'пиздец', 'хуй', 'уебок']) -> bool:
    for word in blacklist:
        if word.lower() in text.lower():
            return True
    return False


@bot.on(event=events.NewMessage)
async def some_message(event: events.NewMessage):
    if find_FUCKING_words(event.text):
        await event.message.delete()
        await event.respond('FUCK YOU')
    else:
        await event.respond('Good job')


if __name__ == '__main__':
    bot.run_until_disconnected()
