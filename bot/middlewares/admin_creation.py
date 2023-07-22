from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher.middlewares import BaseMiddleware
from bot.controllers import user_controller
from bot.models.user import User, StatusChoices
from bot.helpers.config import ADMIN_ID


class AdminCreationMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def on_process_message(self, message: Message, data, *args):
        core_admin = await User.get_user_by_telegram_id(int(ADMIN_ID))

        if core_admin is None:
            try:
                chat_data = await self.bot.get_chat(chat_id=ADMIN_ID)

                await user_controller.make(dict(
                    telegram_id=chat_data.id,
                    name=chat_data.first_name,
                    username=chat_data.username
                ))
            except:
                print("error")

        return
