from dotenv import load_dotenv
from os import environ

load_dotenv()
BOT_TOKEN = environ["TOKEN"]
DB_TYPE = environ['DB_TYPE']
DB_USER = environ['DB_USER']
DB_PASSWORD = environ['DB_PASSWORD']
DB_HOST = environ['DB_HOST']
DB_NAME = environ['DB_NAME']

DB_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


ADMIN_ID = environ['ADMIN_ID']
ADMINS = [ADMIN_ID]

CHANNEL_ID = environ["CHANNEL_ID"]
CHANNEL_LINK = environ['CHANNEL_LINK']
#
# languages_uz = [option['language']['uz'], "uz", 'en']

IS_SUBSCRIBED = "is_subs"