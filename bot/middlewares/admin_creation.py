from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher.middlewares import BaseMiddleware
from bot.controllers import user_controller
from bot.keyboards.keyboard_buttons import option
from bot.models.user import User
from bot.helpers.config import ADMIN_ID


class AdminCreationMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def on_process_message(self, message: Message, data, *args):
        core_admin = await user_controller.get_one(dict(telegram_id=int(ADMIN_ID)))

        if core_admin is None:
            try:
                chat_data = await self.bot.get_chat(chat_id=ADMIN_ID)

                await user_controller.make(dict(
                    telegram_id=chat_data.id,
                    name=chat_data.first_name,
                    username=chat_data.username,
                    type=User.TypeChoices.ADMIN,
                    lang=option['language']['uz']
                ))
            except:
                print("error")

        return
