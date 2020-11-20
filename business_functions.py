from datetime import timedelta
from typing import List
from telethon.tl.functions.channels import EditBannedRequest
from telethon import TelegramClient, events
from telethon.tl.types import (
    User,
    PeerUser,
    ChatBannedRights,
    ChannelParticipantsAdmins,
)

DEF_RIGHTS = ChatBannedRights(until_date=None, send_games=True, send_gifs=True, send_inline=True, send_media=True,
                              send_messages=True,
                              send_polls=True, send_stickers=True, change_info=True, pin_messages=True)


def find_FUCKING_words(text: str, blacklist: List[str] = ['блять', 'пиздец', 'хуй', 'уебок']) -> bool:
    for word in blacklist:
        if word.lower() in text.lower():
            return True
    return False


async def new_user_worker(event: events.NewMessage, bot: TelegramClient):
    await bot(EditBannedRequest(event.chat_id, event.user_id, DEF_RIGHTS))


async def new_message_worker(event: events.NewMessage):
    if find_FUCKING_words(event.text):
        await event.message.delete()
        await event.respond('FUCK YOU')
    else:
        await event.respond('Good job')
