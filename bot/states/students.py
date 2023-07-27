from aiogram.dispatcher.filters.state import StatesGroup, State


class StudentStates(StatesGroup):
    process = State()
    all_students = State()
    one_student = State()