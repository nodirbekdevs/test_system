from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    subject = State()
    name = State()
    description = State()
