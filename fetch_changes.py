import requests
import logging
import hashlib
import os

from telethon.sync import TelegramClient 
from telethon.tl.types import InputPeerUser, InputPeerChannel 
from telethon import TelegramClient, sync, events 


USERS=os.getenv('USERS', '').split('|')
HASH_FILE='hash'

API_ID=os.getenv('TELEGRAM_API_ID')
API_HASH=os.getenv('TELEGRAM_API_HASH')
TOKEN=os.getenv('TELEGRAM_TOKEN')


def send_messages(msg: str) -> None: 
    client: TelegramClient = TelegramClient('notify_users', API_ID, API_HASH).start(bot_token=TOKEN)
    with client:
        for u in USERS:
            client.send_message(u, msg)


def read_hash() -> str:
    try:
        with open(HASH_FILE, 'r+') as f:
            h = f.readline()
    except IOError:
        return None
    return h


def save_hash(content: str) -> None:
    with open(HASH_FILE, 'w') as f:
       f.write(content)


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger = logging.getLogger()

    url = 'https://www.sanita.puglia.it/web/pugliasalute/benvenuto'
    req = requests.get(url, verify=False)
    new_hash = hashlib.sha1(req.text.encode()).hexdigest()
    old_hash = read_hash()
    save_hash(new_hash)
    if old_hash != new_hash:
        send_messages(f'Page {url} has been updated.')

if __name__ == "__main__":
    main()    
