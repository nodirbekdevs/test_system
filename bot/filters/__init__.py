from aiogram import Dispatcher
from bot.filters.is_admin import IsAdmin
from bot.filters.is_instructor import IsInstructor
from bot.filters.is_not_admin import IsNotAdmin
from bot.filters.is_student import IsStudent


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin, event_handlers=[dp.message_handlers, dp.callback_query_handlers])
    dp.filters_factory.bind(IsInstructor, event_handlers=[dp.message_handlers, dp.callback_query_handlers])
    dp.filters_factory.bind(IsNotAdmin, event_handlers=[dp.message_handlers, dp.callback_query_handlers])
    dp.filters_factory.bind(IsStudent, event_handlers=[dp.message_handlers, dp.callback_query_handlers])
