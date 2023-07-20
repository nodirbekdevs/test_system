from aiogram.dispatcher.filters.state import StatesGroup, State


class SectionStates(StatesGroup):
    subject = State()
    name = State()
    description = State()
