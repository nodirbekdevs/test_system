from aiogram.types import Message
from sqlalchemy import column

from bot.loader import dp
from bot.models.user import User
from bot.controllers import user_controller


@dp.message_handler(commands='start')
async def cmd_start(message: Message):
    dope = dict(
        telegram_id=message.from_user.id,
        name=message.from_user.first_name,
        username=message.from_user.username
    )

    # user = await user_controller.make(dict(
    #     telegram_id=message.from_user.id,
    #     name=message.from_user.first_name,
    #     username=message.from_user.username
    # ))

    user = await user_controller.get_one((User.telegram_id==message.from_user.id))

    print(user)
    print(user.type)
    # print(user['type'])

    await message.answer('created')
