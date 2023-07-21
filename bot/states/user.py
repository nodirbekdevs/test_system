from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    instructor_process = State()
    student_process = State()
    subscription = State()
    type = State()
    language = State()
    name = State()
    phone = State()