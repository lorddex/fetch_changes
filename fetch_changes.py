import hashlib
import logging
from typing import Optional

import requests
from telethon import TelegramClient
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from settings import *


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logging.basicConfig(
    level=logging.INFO,
    format='--> %(message)s',
)
logger = logging.getLogger()


def send_messages(msg: str) -> None: 
    if not SEND_MESSAGES:
        return
    client: TelegramClient = TelegramClient(
        'notify_users', API_ID, API_HASH
    ).start(bot_token=TOKEN)
    with client:
        for u in USERS:
            client.send_message(u, msg)


def read_hash(url: str) -> Optional[str]:
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


def validate() -> bool:
    if not SEND_MESSAGES:
        logger.info(
            'Messages disabled, set the environment var to SEND_MESSAGES=True to enable them.'
        )
        return True
    if not API_ID:
        logger.error('API_ID must be set in order to send messages.')
        return False
    if not API_HASH:
        logger.error('API_HASH must be set in order to send messages.')
        return False
    if not TOKEN:
        logger.error('TOKEN must be set in order to send messages.')
        return False
    return True


def main() -> None:
    if not validate():
        return

    for url in URLS:
        logger.info(f'Fetching {url}')
        req = requests.get(url, verify=False)
        new_hash = hashlib.sha1(req.text.encode()).hexdigest()
        old_hash = read_hash(url)
        save_hash(new_hash, url)
        if old_hash != new_hash:
            logger.info(
                f' - Old Hash {old_hash}, New Hash: {new_hash}, {url} updated.'
            )
            send_messages(f'Page {url} has been updated.')


if __name__ == "__main__":
    main()    
