from aiogram.types import Message
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from bot.controllers import user_controller
from bot.helpers.config import ADMIN_ID, ADMINS, CHANNEL_ID, CHANNEL_LINK
from bot.helpers.utils import is_subscribed
from bot.keyboards.keyboards import is_subscribed_keyboard


class ChannelSubscriptionMiddleware(BaseMiddleware):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.channel_id = CHANNEL_ID

    async def on_process_message(self, message: Message, data, *args):
        language_code = message.from_user.language_code

        if message.from_user.id in ADMINS:
            return 

        is_subs = await is_subscribed(bot=self.bot, message=message, CHANNEL_ID=CHANNEL_ID)

        if not is_subs:
            message_text = "Kanalga obuna bo'ling, aks holda bot ishlamaydi 👌" \
                if language_code == 'uz' or language_code == 'en' else \
                'Пожалуйста подпишитесь на канал, иначе бот не будет работать 👌'

            await self.bot.send_message(
                chat_id=message.from_user.id,
                text=message_text,
                reply_markup=is_subscribed_keyboard(language_code, CHANNEL_LINK),
            )
            raise CancelHandler()

        return