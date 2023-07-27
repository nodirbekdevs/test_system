from aiogram.dispatcher.filters.state import StatesGroup, State


class SubjectStates(StatesGroup):
    process = State()
    all_subjects = State()
    one_subject = State()
    name = State()
    description = State()
    checking = State()
