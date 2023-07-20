from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat

from bot.controllers import user_controller
from bot.models.user import User

commands = [
    BotCommand(command="start", description="Запустить"),
]

admin_commands = [
    *commands,
    BotCommand(command="send_all", description="Рассылка сообщений ползовательям"),
    BotCommand(command="activity", description="Данные")
]


async def set_default_commands(bot: Bot):
    await bot.delete_my_commands()

    await bot.set_my_commands(commands=commands)

    admins = await user_controller.get_one((User.type == User.TypeChoices.ADMIN))

    if admins:
        for admin in admins:
            await bot.set_my_commands(commands=admin_commands, scope=BotCommandScopeChat(chat_id=admin.telegram_id))
