from dotenv import load_dotenv
from os import environ
from bot.keyboards.keyboard_buttons import option

load_dotenv()
BOT_TOKEN = environ["TOKEN"]
POSTGRES_TYPE = environ['POSTGRES_TYPE']
POSTGRES_USER = environ['POSTGRES_USER']
POSTGRES_PASSWORD = environ['POSTGRES_PASSWORD']
POSTGRES_HOST = environ['POSTGRES_HOST'] if environ['POSTGRES_HOST'] == 'db' else 'localhost'
POSTGRES_DB = environ['POSTGRES_DB']
POSTGRES_PORT = environ['POSTGRES_PORT']

GET, POST, PUT, DELETE, COUNT, SINGLE, ALL = 'GET', 'POST', 'PUT', 'DELETE', 'COUNT', 'SINGLE', 'ALL'

ADMIN, INSTRUCTOR, STUDENT, SECTION, TEST, SUBJECT = 'ADMIN', 'INSTRUCTOR', 'STUDENT', 'SECTION', 'TEST', 'SUBJECT'

SEEN, DONE = 'SEEN', 'DONE'

UZ, RU = 'uz', 'ru'

DB_URL = f"{POSTGRES_TYPE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


ADMIN_ID = environ['ADMIN_ID']
ADMINS = [ADMIN_ID]

CHANNEL_ID = environ["CHANNEL_ID"]
CHANNEL_LINK = environ['CHANNEL_LINK']

languages_uz = [option['language']['uz'], "uz", 'en']

IS_SUBSCRIBED = "is_subs"