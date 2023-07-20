from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from bot.controllers import user_controller
from bot.models.user import User


class IsStudent(BoundFilter):
    async def check(self, message: Message):
        student = await user_controller.get_one(dict(telegram_id=message.from_user.id))

        if student.type != User.TypeChoices.STUDENT:
            return False

        return True
