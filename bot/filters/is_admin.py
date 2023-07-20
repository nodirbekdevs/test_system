from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from bot.controllers import user_controller
from bot.models.user import User


class IsAdmin(BoundFilter):
    async def check(self, message: Message):
        admin = await user_controller.get_one(dict(telegram_id=message.from_user.id))

        if admin.type != User.TypeChoices.ADMIN:
            return False

        return True
