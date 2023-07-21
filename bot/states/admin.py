from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    process = State()
    type = State()
    language = State()
    name = State()
    phone = State()