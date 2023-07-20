from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from bot.controllers import user_controller
from bot.models.user import User


class IsTeacher(BoundFilter):
    async def check(self, message: Message):
        teacher = await user_controller.get_one(dict(telegram_id=message.from_user.id))

        if teacher.type != User.TypeChoices.INSTRUCTOR:
            return False

        return True