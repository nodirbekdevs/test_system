from aiogram import executor, Dispatcher
from logging import INFO

from bot.loader import dp, bot, logger
from bot.db.database import db
from bot.helpers.config import DB_URL

from bot.handlers import onboarding, register, settings, feedback, main

from bot.filters import setup
from bot.middlewares.admin_creation import AdminCreationMiddleware
from bot.commands.default_commands import set_default_commands
from bot.middlewares.channel_subscription import ChannelSubscriptionMiddleware

dp.setup_middleware(AdminCreationMiddleware(bot=bot))
# dp.setup_middleware(ChannelSubscriptionMiddleware(bot=bot, channel_id=CHANNEL_ID))
setup(dp)


async def startup(dispatcher: Dispatcher):
    logger.info(DB_URL)
    await db.set_bind(DB_URL)
    await db.gino.create_all()
    await set_default_commands(dispatcher=dispatcher)
    logger.info("DB connected")
    logger.info(INFO)
    logger.warning("Bot started")


async def shutdown(dispatcher):
    logger.warning("Shutting down..")
    await db.pop_bind().close()
    logger.warning("Bot down")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown, skip_updates=True)
