from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from bot.loader import dp

from bot.filters.is_not_admin import IsNotAdmin
from bot.models.user import User
from bot.keyboards.keyboards import instructor_pages_keyboard, student_pages_keyboard
from bot.keyboards.keyboard_buttons import option
from bot.helpers.utils import is_num, translator
from bot.states.user import UserStates


@dp.callback_query_handler(lambda query: query.data == 'none', state='*')
async def paginate_handler(query: CallbackQuery, state: FSMContext):
    user = await User.get_user_by_telegram_id(query.from_user.id)

    message_text = translator(
        "Bu yerda ma'lumotlar yo'q. Siz noto'g'ri betni tanladingiz.",
        "Здесь нет данных. Вы выбрали не ту страницу.",
        user.lang
    )

    await query.answer(text=message_text, show_alert=True)


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


async def num_error_handler(message: Message, type, language):
    checking, message_text = True, ''

    if type == 'NUM':
        checking = is_num(message.text)
    elif type == 'NAN':
        checking = not is_num(message.text)


