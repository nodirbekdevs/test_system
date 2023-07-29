from aiogram.dispatcher.filters.state import StatesGroup, State


class AdvertisingStates(StatesGroup):
    process = State()
    all_advertisements = State()
    one_advertising = State()
    image = State()
    title = State()
    description = State()
    checking = State()