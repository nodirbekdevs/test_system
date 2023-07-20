from aiogram.dispatcher.filters.state import StatesGroup, State


class TestStates(StatesGroup):
    subject = State()
    section = State()
    question = State()
    variants = State()
    correct_answer = State()
