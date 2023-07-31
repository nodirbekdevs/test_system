from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from bot.loader import dp
from bot.filters.is_not_admin import IsNotAdmin
from bot.models.user import User
from bot.keyboards.keyboard_buttons import option
from bot.keyboards.keyboards import student_pages_keyboard, instructor_pages_keyboard
from bot.helpers.utils import translator
from bot.states.user import UserStates


@dp.message_handler(IsNotAdmin(), text=[option['main']['uz'], option['main']['ru']], state='*')
async def user_main_handler(message: Message, state: FSMContext):
    user = await User.get_user_by_telegram_id(message.from_user.id)

    message_text = translator('Bosh sahifa', 'Домашняя страница', user.lang)

    await UserStates.process.set()

    keyboard = []

    if user.type == User.TypeChoices.INSTRUCTOR:
        keyboard = instructor_pages_keyboard(user.lang)
    elif user.type == User.TypeChoices.STUDENT:
        keyboard = student_pages_keyboard(user.lang)

    await message.answer(message_text, reply_markup=keyboard)