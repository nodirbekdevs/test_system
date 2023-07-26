from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot.loader import dp
from bot.controllers import user_controller
from bot.filters.is_admin import IsAdmin
from bot.keyboards.keyboard_buttons import option
from bot.keyboards.keyboards import admin_pages_keyboard
from bot.states.user import UserStates


@dp.message_handler(IsAdmin(), text=[option['start'], option['main']['uz'], option['main']['ru']], state='*')
async def admin_main_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    await UserStates.process.set()

    message_text = "Bosh sahifa" if user.lang == option['language']['uz'] else 'Главная страница'

    await message.answer(message_text, reply_markup=admin_pages_keyboard(user.lang))


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == 'none', state='*')
async def paginate_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    message_text = "Bu yerda ma'lumotlar yo'q. Siz noto'g'ri betni tanladingiz." \
        if user.lang == option['language']['uz'] else \
        "Здесь нет информации. Вы выбрали не ту страницу."

    await query.answer(text=message_text, show_alert=True)