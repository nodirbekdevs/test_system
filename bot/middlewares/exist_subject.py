from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from bot.controllers import subject_controller, user_controller
from bot.keyboards.keyboard_buttons import option
from bot.models.user import User
from bot.models.subject import StatusChoices
from bot.helpers.config import ADMIN_ID
from bot.helpers.utils import translator


class AdminCreationMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    @classmethod
    async def on_process_message(self, message: Message, data, *args):
        user = await user_controller.get_one(dict(telegram_id=int(ADMIN_ID)))

        subjects = await subject_controller.get_all(dict(status=StatusChoices.ACTIVE))

        if user is None and subjects == 0:
            if len(subjects) == 0:
                await message.answer('Hozircha botda ishlar tugatilmagan\nБот еще не доработан')
                raise CancelHandler()

        return
