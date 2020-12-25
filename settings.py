import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

USERS = os.getenv('USERS', '').split('|')
URLS = os.getenv('URLS', '').split('|')

SEND_MESSAGES = bool(os.getenv('SEND_MESSAGES', False))
API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
TOKEN = os.getenv('TELEGRAM_TOKEN')
