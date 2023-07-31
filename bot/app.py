from aiogram import executor, Dispatcher
from logging import INFO

from bot.loader import dp, bot, logger
from bot.db.database import db
from bot.helpers.config import DB_URL

from bot.handlers import onboarding, register, settings, feedback, main
from bot.handlers.admin import advertisements, feedback, admins, instructors, subjects
from bot.handlers.instructor import sections, tests

from bot.filters import setup
from bot.middlewares.admin_creation import AdminCreationMiddleware
from bot.middlewares.channel_subscription import ChannelSubscriptionMiddleware
from bot.middlewares.is_active import IsActive

from bot.commands.default_commands import set_default_commands

dp.setup_middleware(AdminCreationMiddleware(bot=bot))
# dp.setup_middleware(ChannelSubscriptionMiddleware(bot=bot, channel_id=CHANNEL_ID))
# dp.setup_middleware(IsActive(bot=bot))
setup(dp)


async def startup(dispatcher: Dispatcher):
    logger.info(DB_URL)
    await db.set_bind(DB_URL)
    await db.gino.create_all()
    await set_default_commands(dispatcher=dispatcher)
    logger.info("DB connected")
    logger.info(INFO)
    logger.warning("Bot started")


async def shutdown(dispatcher: Dispatcher):
    logger.warning("Shutting down..")
    await db.pop_bind().close()
    logger.warning("Bot down")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown, skip_updates=True)
