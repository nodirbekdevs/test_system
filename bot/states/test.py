from aiogram.dispatcher.filters.state import StatesGroup, State


class TestStates(StatesGroup):
    process = State()
    all_tests = State()
    one_test = State()
    image = State()
    subject = State()
    section = State()
    question = State()
    variants = State()
    correct_answer = State()
    checking = State()
