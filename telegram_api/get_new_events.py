import configparser
from datetime import datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.patched import Message
from telethon.tl.types import (
    MessageEntityTextUrl
)
from telethon.tl.functions.messages import (GetHistoryRequest)

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)


def create_message(message: Message):
    textWithUrls = message.message
    urls = list(filter(lambda x: isinstance(x, MessageEntityTextUrl), message.entities))
    for entity in message.entities:
        print(isinstance(entity, MessageEntityTextUrl))
    urls = sorted(urls, key=lambda x: x.offset, reverse=True)
    for url in urls:
        print(textWithUrls[url.offset: url.offset + url.length])
        textWithUrls = \
            textWithUrls[: url.offset] + \
            "<a href=" + url.url + ">" + \
            textWithUrls[url.offset:url.offset + url.length] + \
            "<\\a>" + \
            textWithUrls[url.offset + url.length:]
    return textWithUrls


async def get_new_events(link: str, lastUpdate: datetime):
    client.start()
    print("Client Created")

    if not await client.is_user_authorized():
        await authorize()

    channel = await client.get_entity(link)

    offset_id = 0

    messages = await client(GetHistoryRequest(
        peer=channel,
        offset_id=offset_id,
        offset_date=lastUpdate,
        add_offset=0,
        limit=3,
        max_id=0,
        min_id=0,
        hash=0
    ))
    return map(create_message, messages.messages[1:])


async def authorize():
    # Ensure you're authorized
    await client.send_code_request(phone)
    try:
        await client.sign_in(phone, input('Enter the code: '))
    except SessionPasswordNeededError:
        await client.sign_in(password=input('Password: '))
