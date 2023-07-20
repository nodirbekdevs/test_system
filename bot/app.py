from aiogram import executor

from asyncio import get_event_loop
from logging import INFO

from bot.loader import dp, bot, logger
from bot.db.database import db
from bot.helpers.config import DB_URL

from bot.handlers import onboarding

from bot.filters import setup
from bot.middlewares.admin_creation import AdminCreationMiddleware
from bot.commands.default_commands import set_default_commands
from bot.middlewares.channel_subscription import ChannelSubscriptionMiddleware

dp.setup_middleware(AdminCreationMiddleware(bot=bot))
setup(dp)


async def on_startup():
    await db.set_bind(DB_URL)
    await db.gino.create_all()
    logger.info("DB connected")
    logger.info(INFO)
    logger.warning("Bot started")


async def on_shutdown():
    logger.warning("Shutting down..")
    await db.pop_bind().close()
    logger.warning("Bot down")


if __name__ == '__main__':
    # dp.setup_middleware(ChannelSubscriptionMiddleware(bot=bot, channel_id=CHANNEL_ID))
    get_event_loop().run_until_complete(set_default_commands(bot=bot))
    get_event_loop().run_until_complete(on_startup())
    get_event_loop().run_until_complete(on_startup())
    executor.start_polling(dp, skip_updates=True)
