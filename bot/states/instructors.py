from aiogram.dispatcher.filters.state import StatesGroup, State


class InstructorStates(StatesGroup):
    process = State()
    all_instructors = State()
    one_instructor = State()
    add = State()
    type = State()
    language = State()
    name = State()
    phone = State()