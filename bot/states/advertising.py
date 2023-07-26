from aiogram.dispatcher.filters.state import StatesGroup, State


class AdvertisingStates(StatesGroup):
    process = State()
    pagination = State()
    single = State()
    image = State()
    title = State()
    description = State()
    checking = State()