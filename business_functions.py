from typing import List
from telethon.tl.functions.channels import EditBannedRequest, GetChannelsRequest
from telethon import TelegramClient, events
import db_worker
from telethon.tl.types import User, PeerUser, ChatBannedRights, ChannelParticipantsAdmins, PeerChannel

db_worker.create()

DEF_RIGHTS = ChatBannedRights(until_date=None, send_games=True, send_gifs=True, send_inline=True, send_media=True,
                              send_messages=True,
                              send_polls=True, send_stickers=True, change_info=True, pin_messages=True)


def find_blacklisted_words(text: str, blacklist: List[str] = ['блять', 'пиздец', 'хуй', 'уебок']) -> bool:
    for word in blacklist:
        if word.lower() in text.lower():
            return True
    return False


async def new_user_worker(event: events.ChatAction, bot: TelegramClient):
    await bot(EditBannedRequest(event.chat_id, event.user_id, DEF_RIGHTS))


async def after_verification(event: events.NewMessage, bot: TelegramClient):
    for chat_id in db_worker.Chats.get_all():
        chat = await bot.get_entity(PeerChannel(chat_id.tg_id))
        await bot(EditBannedRequest(chat_id.tg_id, event.message.sender.id, chat.default_banned_rights))


async def start_msg(event: events.NewMessage):
    if not db_worker.Student.has_authorized(event.message.sender.id):
        await event.respond('Чтобы получить доступ к чату пройдите верификацию: ФИО')
    else:
        await event.respond('Вы уже авторизованы')


async def new_message_worker(event: events.NewMessage, bot: TelegramClient):
    if event.text.startswith('/start'):
        return
    if len(event.text.split(' ')) == 3:
        student = db_worker.Student.get_by_fio(event.text.split(' ')[0], event.text.split(' ')[1],
                                               event.text.split(' ')[2])
        if student is not None:
            if student.tg_id is None:
                student.set_tg_id(event.message.sender.id)
                await after_verification(event, bot)
                return
            else:
                await event.respond('Это пользователь занят')
    if find_blacklisted_words(event.text):
        await event.message.delete()
        await event.respond('FUCK YOU')
    else:
        await event.respond('Good job')
