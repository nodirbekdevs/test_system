from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    process = State()
    all_admins = State()
    one_admin = State()
    add = State()
    type = State()
    language = State()
    name = State()
    phone = State()