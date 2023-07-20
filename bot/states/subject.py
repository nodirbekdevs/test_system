from aiogram.dispatcher.filters.state import StatesGroup, State


class SubjectStates(StatesGroup):
    name = State()
    description = State()
