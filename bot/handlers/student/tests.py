import aiofiles
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentTypes

from deep_translator import GoogleTranslator
from os import mkdir, remove
from os.path import join, abspath, dirname, exists
from asyncio import to_thread

from bot.loader import dp
from bot.controllers import user_controller, section_controller, test_controller, subject_controller
from bot.models.user import User
from bot.models.test import StatusChoices
from bot.keyboards.keyboards import instructor_keyboard, one_instructor_keyboard, subjects_sections_keyboard, \
    confirmation_keyboard, next_keyboard, back_keyboard
from bot.filters.is_instructor import IsInstructor
from bot.keyboards.keyboard_buttons import instructor, option
from bot.helpers.utils import Pagination, is_num, translator
from bot.helpers.formats import test_format
from bot.helpers.config import TEST
from bot.states.test import TestStates
from bot.states.user import UserStates