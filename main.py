from typing import List
from pathlib import Path
from os import environ
from telethon import TelegramClient, events
from datetime import timedelta
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (
    User,
    PeerUser,
    ChatBannedRights,
    ChannelParticipantsAdmins,
)

DEF_RIGHTS = ChatBannedRights(until_date=None, send_games=True, send_gifs=True, send_inline=True, send_media=True, send_messages=True,
                              send_polls=True, send_stickers=True, change_info=True, pin_messages=True)


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


def find_FUCKING_words(text: str, blacklist: List[str] = ['блять', 'пиздец', 'хуй', 'уебок']) -> bool:
    for word in blacklist:
        if word.lower() in text.lower():
            return True
    return False

@bot.on(events.ChatAction)
async def new_user(event: events.ChatAction):
    if event.user_joined:
        await event.respond('New user')

@bot.on(event=events.NewMessage)
async def some_message(event: events.NewMessage):
    if find_FUCKING_words(event.text):
        await event.message.delete()
        await event.respond('FUCK YOU')
    else:
        await event.respond('Good job')


if __name__ == '__main__':
    bot.run_until_disconnected()
