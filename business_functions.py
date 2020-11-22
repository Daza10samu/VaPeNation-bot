from typing import List
from datetime import timedelta
from datetime import datetime
from telethon.tl.functions.channels import EditBannedRequest, GetChannelsRequest, GetParticipantsRequest
from telethon import TelegramClient, events
import db_worker
from blacklist import blacklister
from telethon.tl.types import User, PeerUser, ChatBannedRights, ChannelParticipantsAdmins, PeerChannel
from os import environ
from pathlib import Path

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

db_worker.create(environ)

DEF_RIGHTS = ChatBannedRights(until_date=None, send_games=True, send_gifs=True, send_inline=True, send_media=True,
                              send_messages=True,
                              send_polls=True, send_stickers=True, change_info=True, pin_messages=True)


def find_blacklisted_words(text: str) -> bool:
    return blacklister(text)


async def new_user_worker(event: events.ChatAction, bot: TelegramClient):
    if db_worker.Student.has_authorized(event.user_id):
        await bot(EditBannedRequest(event.chat_id, event.user_id, event.chat.default_banned_rights))
    else:
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
    admins = await get_admin_list(event.chat, bot)
    if event.text.startswith('/start'):
        return
    if event.text.startswith('/getinfo') and event.sender in admins:
        if event.message.reply_to is not None:
            user = db_worker.Student.get_by_tg_id((await event.get_reply_message()).sender_id)
            if user is not None:
                await event.respond(f'{user.surname} {user.name} {user.secondname}')
            else:
                await event.respond('К этому аккаунту не привязан пользователь')
        elif len(event.text.split()) == 4:
            user = db_worker.Student.get_by_fio(name=event.text.split()[2], surname=event.text.split()[1],
                                                secondname=event.text.split()[3])
            if user is not None and user.tg_id is not None:
                user_tg = await bot.get_entity(user.tg_id)
                await event.respond(f'@{user_tg.username} {user_tg.id}')
            else:
                await event.respond('К этому аккаунту не привязан пользователь')
        else:
            await event.respond('Неверный формат запроса')
    if event.text.startswith('/mute') and event.sender in admins:
        await bot(EditBannedRequest(event.chat.id, (await event.get_reply_message()).sender_id,
                                    ChatBannedRights(
                                        until_date=datetime.now() + timedelta(minutes=int(event.text.split()[1])),
                                        send_games=True, send_gifs=True, send_inline=True,
                                        send_media=True,
                                        send_messages=True,
                                        send_polls=True, send_stickers=True, change_info=True,
                                        pin_messages=True)))
        await (await event.get_reply_message()).delete()
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


async def get_admin_list(chat, bot: TelegramClient):
    admins = []
    async for admin in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        admins.append(admin)
    return admins
