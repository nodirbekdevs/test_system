from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from bot.loader import bot, dp
from bot.controllers import user_controller
from bot.models.user import User
from bot.helpers.config import CHANNEL_ID, languages_uz, IS_SUBSCRIBED
from bot.helpers.utils import is_subscribed, translator
from bot.helpers.formats import introduction_format
from bot.keyboards.keyboards import instructor_pages_keyboard, student_pages_keyboard, language_keyboard
from bot.states.user import UserStates


# @dp.callback_query_handler(lambda query: query.data == IS_SUBSCRIBED, state='*')
# async def check_is_subscribed(query: CallbackQuery, state: FSMContext):
#     user = await user_controller.get_one(dict(telegram_id=query.from_user.id))
#
#     if not await is_subscribed(bot, query.message, CHANNEL_ID):
#         language_code = user.lang if user else query.from_user.language_code
#
#         message_text = "Siz kanalga obuna bo'lmagansiz" if language_code in languages_uz else "Вы не подписаны на канал"
#
#         await query.answer(text=message_text, show_alert=True)
#
#         await UserStates.subscription.set()
#         return
#
#     await query.message.delete()
#
#     message_text, keyboard = translator('Bosh sahifa', 'Домашняя страница', user.lang), []
#
#     await UserStates.process.set()
#
#
#     if user.type == User.TypeChoices.STUDENT:
#         keyboard = student_pages_keyboard(user.lang)
#
#     if user.type == User.TypeChoices.INSTRUCTOR:
#         keyboard = instructor_pages_keyboard(user.lang)
#
#     await UserStates.language.set()
#
#     await query.message.answer(introduction_format(query.from_user.first_name), reply_markup=language_keyboard())
