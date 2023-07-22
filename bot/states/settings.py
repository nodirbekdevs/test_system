from aiogram.dispatcher.filters.state import StatesGroup, State


class SettingsStates(StatesGroup):
    process = State()
    name = State()
    number = State()
    lang = State()