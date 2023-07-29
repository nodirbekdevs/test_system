from aiogram.dispatcher.filters.state import StatesGroup, State


class FeedbackStates(StatesGroup):
    process = State()
    active_feedback = State()
    one_active_feedback = State()
    seen_feedback = State()
    one_seen_feedback = State()
    mark = State()
    reason = State()