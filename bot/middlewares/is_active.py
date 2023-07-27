from aiogram.types import Message
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from bot.controllers import user_controller


class IsActive(BaseMiddleware):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @classmethod
    async def on_process_message(self, message: Message, data, *args):
        user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

        if not user:
            raise CancelHandler()

        return
