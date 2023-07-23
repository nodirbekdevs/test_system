from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from bot.loader import dp
from bot.models.user import User
from bot.keyboards.keyboard_buttons import option


@dp.callback_query_handler(lambda query: query.data == 'none', state='*')
async def paginate_handler(query: CallbackQuery, state: FSMContext):
    user = await User.get_user_by_telegram_id(query.from_user.id)

    message_text = "Bu yerda ma'lumotlar yo'q. Siz noto'g'ri betni tanladingiz." \
        if user.lang == option['language']['uz'] else \
            "Здесь нет данных. Вы выбрали не ту страницу."

    await query.answer(text=message_text, show_alert=True)