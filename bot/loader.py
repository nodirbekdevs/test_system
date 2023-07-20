from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.helpers.config import BOT_TOKEN
from bot.helpers.custom_logger import custom_logger

logger = custom_logger('global', "INFO")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())