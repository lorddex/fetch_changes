import requests
import logging
import hashlib
import os

from dotenv import load_dotenv
from telethon.sync import TelegramClient 
from telethon.tl.types import InputPeerUser, InputPeerChannel 
from telethon import TelegramClient, sync, events 


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

USERS = os.getenv('USERS', '').split('|')
URLS = os.getenv('URLS', '').split('|')

API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
TOKEN = os.getenv('TELEGRAM_TOKEN')


def send_messages(msg: str) -> None: 
    client: TelegramClient = TelegramClient('notify_users', API_ID, API_HASH).start(bot_token=TOKEN)
    with client:
        for u in USERS:
            client.send_message(u, msg)


def read_hash(url: str) -> str:
    url_hash = hashlib.sha1(url.encode()).hexdigest()
    try:
        with open(f'{url_hash}.hash', 'r+') as f:
            h = f.readline()
    except IOError:
        return None
    return h


def save_hash(content: str, url: str) -> None:
    url_hash = hashlib.sha1(url.encode()).hexdigest()
    with open(f'{url_hash}.hash', 'w') as f:
       f.write(content)


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger = logging.getLogger()
    
    for url in URLS:
        req = requests.get(url, verify=False)
        new_hash = hashlib.sha1(req.text.encode()).hexdigest()
        old_hash = read_hash(url)
        save_hash(new_hash, url)
        if old_hash != new_hash:
            send_messages(f'Page {url} has been updated.')

if __name__ == "__main__":
    main()    
