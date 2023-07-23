from aiogram.dispatcher.filters.state import StatesGroup, State


class SectionStates(StatesGroup):
    process = State()
    all_sections = State()
    one_section = State()
    subject = State()
    name = State()
    description = State()
    checking = State()
