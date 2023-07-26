from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from bot.controllers import user_controller
from bot.models.user import User


class IsNotAdmin(BoundFilter):
    async def check(self, message: Message):
        user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

        if user.type == User.TypeChoices.ADMIN:
            return False

        return True