from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from bot.loader import dp, bot
from bot.models.feedback import StatusChoices
from bot.controllers import feedback_controller, user_controller
from bot.filters.is_admin import IsAdmin
from bot.helpers.formats import feedback_all_format, feedback_format, feedback_seen_format, feedback_done_format
from bot.helpers.utils import Pagination
from bot.keyboards.keyboard_buttons import admin, option
from bot.keyboards.keyboards import (
    admin_pages_keyboard, admin_feedback_keyboard, one_seen_feedback_keyboard, one_done_feedback_keyboard
)
from bot.states.user import UserStates
from bot.states.feedback import FeedbackStates


@dp.message_handler(
    IsAdmin(), text=[admin['pages']['uz']['feedback'], admin['pages']['ru']['feedback']], state=UserStates.process
)
async def feedback_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))
    await FeedbackStates.process.set()
    message_text = 'Izohlar sahifasi' if user.lang == option['language']['uz'] else "Страница комментариев"

    await message.answer(message_text, reply_markup=admin_feedback_keyboard(user.lang))


@dp.message_handler(
    IsAdmin(), text=[admin['feedback']['uz']['number'], admin['feedback']['ru']['number']], state=FeedbackStates.process
)
async def number_of_all_feedback_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    count = await feedback_controller.count(dict())
    active = await feedback_controller.count(dict(status=StatusChoices.ACTIVE))
    seen = await feedback_controller.count(dict(status=StatusChoices.SEEN))
    done = await feedback_controller.count(dict(status=StatusChoices.DONE))

    await message.answer(
        feedback_all_format(dict(count=count, active=active, seen=seen, done=done)),
        reply_markup=admin_feedback_keyboard(user.lang)
    )


@dp.message_handler(IsAdmin(), text=admin['feedback']['read'], state=FeedbackStates.process)
async def active_feedback_pagination_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    paginated = await Pagination('FEEDBACK').paginate(
        page=1, limit=6, query=dict(is_read=False, status=StatusChoices.ACTIVE), language=user.lang
    )

    await FeedbackStates.active_pagination.set()

    await message.answer(paginated['message'], reply_markup=paginated['keyboard'])

    if not paginated['status']:
        await FeedbackStates.process.set()
        await message.answer("Hozirgacha yozilgan yangi izohlar")


@dp.callback_query_handler(
    IsAdmin(),
    lambda query: query.data.startswith("left#selfeedback#") or query.data.startswith("right#selfeedback#"),
    state=FeedbackStates.active_pagination
)
async def paginate_feedback_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    paginated = await Pagination('FEEDBACK').paginate(
        int(query.data.split('#')[2]), 6, dict(is_read=False, status=StatusChoices.ACTIVE), user.lang
    )

    if not paginated['status']:
        FeedbackStates.process.set()

    await query.message.edit_text(paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == 'delete', state=FeedbackStates.active_pagination)
async def back_from_feedback_pagination_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    await query.message.delete()
    await FeedbackStates.process.set()

    message_text = 'Izohlar sahifasi' if user.lang == option['language']['uz'] else "Страница комментариев"

    await query.message.answer(message_text, reply_markup=admin_feedback_keyboard(user.lang))


@dp.callback_query_handler(IsAdmin(), lambda query: query.data.startswith("se_feed-"),
                           state=FeedbackStates.active_pagination)
async def get_single_active_feedback_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    _id = query.data.split("-")[1]

    feedback = await feedback_controller.get_one(dict(id=int(_id)))
    author = await user_controller.get_one(dict(id=feedback.user_id))

    await FeedbackStates.one_active_feedback.set()

    dope = dict(
        author=author['name'],
        mark=feedback['mark'],
        reason=feedback['reason'],
        status=feedback['status'],
        created_at=feedback['created_at'].strftime('%d.%m.%Y %H:%M')
    )

    await query.message.edit_text(
        text=feedback_format(dope, user.lang),
        reply_markup=one_seen_feedback_keyboard(feedback['_id'], feedback['mark'], user.lang)
    )


@dp.callback_query_handler(IsAdmin(), lambda query: query.data.startswith("s_d."),
                           state=FeedbackStates.one_active_feedback)
async def done_single_feedback_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    id = query.data.split(".")[1]

    feedback = await feedback_controller.get_one(dict(id=int(id)))
    author = await user_controller.get_one(dict(id=feedback.user_id))

    dope = dict(name=author['name'], feedback=feedback['reason'])

    if feedback.status == StatusChoices.ACTIVE:
        await feedback_controller.update(dict(id=feedback.id), dict(is_read=True, status=StatusChoices.DONE))

    await bot.send_message(author.telegram_id, feedback_done_format(dope, author.lang))

    message_text = "Muommo ko'rildi" if user.lang == option['language']['uz'] else "Обнаружена проблема"

    await query.message.answer(message_text)

    await FeedbackStates.active_pagination.set()

    paginated = await Pagination('FEEDBACK').paginate(1, 6, dict(is_read=False, status=StatusChoices.ACTIVE), user.lang)

    if not paginated['status']:
        await FeedbackStates.process.set()

    await query.message.edit_text(paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(
    IsAdmin(), lambda query: query.data.startswith("seen."), state=FeedbackStates.one_active_feedback
)
async def seen_single_feedback_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    _id = query.data.split(".")[1]

    feedback = await feedback_controller.get_one(dict(id=int(_id)))
    author = await user_controller.get_one(dict(id=feedback.user_id))

    dope = dict(name=author['name'], feedback=feedback['reason'])

    if feedback.status == StatusChoices.ACTIVE:
        await feedback_controller.update(dict(id=feedback.id), dict(is_read=True, status=StatusChoices.SEEN))

    await bot.send_message(author['telegram_id'], feedback_seen_format(dope, author.lang))

    message_text = "Bu izoh ustida ishlar boshlandi" \
        if user.lang == option['language']['uz'] else \
        "Работа над этим комментарием началась"

    await query.message.answer(message_text)

    await FeedbackStates.active_pagination.set()

    paginated = await Pagination('FEEDBACK').paginate(1, 6, dict(is_read=False, status=StatusChoices.ACTIVE), user.lang)

    await query.message.delete()

    if not paginated['status']:
        await FeedbackStates.process.set()

    await query.message.edit_text(paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == 'back', state=FeedbackStates.one_active_feedback)
async def back_from_single_feedback_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    await FeedbackStates.active_pagination.set()

    paginated = await Pagination('FEEDBACK').paginate(1, 6, dict(is_read=False, status=StatusChoices.ACTIVE), user.lang)

    if not paginated['status']:
        await FeedbackStates.process.set()

    await query.message.edit_text(paginated['message'], reply_markup=paginated['keyboard'])


@dp.message_handler(
    IsAdmin(), text=[admin['feedback']['uz']['doing'], admin['feedback']['ru']['doing']], state=FeedbackStates.process
)
async def seen_feedback_pagination_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    await FeedbackStates.seen_pagination.set()
    paginated = await Pagination('FEEDBACK').paginate(1, 6, dict(is_read=True, status=StatusChoices.SEEN), user.lang)

    if not paginated['status']:
        await FeedbackStates.process.set()

    await message.answer(paginated['message'], reply_markup=paginated['keyboard'])

    message_text = "Hozirgacha bajarilayotgan izohlar" \
        if user.lang == option['language']['uz'] else \
        "Комментарии в процессе до сих пор"

    await message.answer(message_text)


@dp.callback_query_handler(
    IsAdmin(),
    lambda query: query.data.startswith("left#dofeedback#") or query.data.startswith("right#dofeedback#"),
    state=FeedbackStates.seen_pagination
)
async def paginate_seen_feedback_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    paginated = await Pagination('FEEDBACK').paginate(
        int(query.data.split('#')[2]), 6, dict(is_read=True, status=StatusChoices.SEEN), user.lang
    )

    await query.message.edit_text(paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == 'delete', state=FeedbackStates.seen_pagination)
async def back_from_feedback_pagination_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    await query.message.delete()
    await FeedbackStates.process.set()

    message_text = 'Izohlar sahifasi' if user.lang == option['language']['uz'] else "Страница комментариев"

    await query.message.answer(message_text, reply_markup=admin_feedback_keyboard(user.lang))


@dp.callback_query_handler(
    IsAdmin(), lambda query: query.data.startswith("do_feed-"), state=FeedbackStates.seen_pagination
)
async def get_single_active_feedback_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    id = query.data.split("-")[1]

    feedback = await feedback_controller.get_one(dict(id=int(id)))
    author = await user_controller.get_one(dict(id=feedback.user_id))

    dope = dict(
        author=author['name'],
        mark=feedback['mark'],
        reason=feedback['reason'],
        status=feedback['status'],
        created_at=feedback['created_at'].strftime('%d.%m.%Y %H:%M')
    )

    await FeedbackStates.one_seen_feedback.set()

    await query.message.edit_text(
        text=feedback_format(dope, user.lang), reply_markup=one_done_feedback_keyboard(feedback['_id'], user.lang)
    )


@dp.callback_query_handler(
    IsAdmin(), lambda query: query.data.startswith("done."), state=FeedbackStates.one_seen_feedback
)
async def done_single_feedback_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    id = query.data.split("-")[1]

    feedback = await feedback_controller.get_one(dict(id=int(id)))
    author = await user_controller.get_one(dict(id=feedback.user_id))

    dope = dict(name=author['name'], feedback=feedback['reason'])

    if feedback.status == StatusChoices.SEEN:
        await feedback_controller.update(dict(id=feedback.id), dict(is_read=True, status=StatusChoices.DONE))

    await bot.send_message(author.telegram_id, feedback_done_format(dope, author.lang))

    message_text = "Muommoni hal qilindi" if user.lang == option['language']['uz'] else "Проблема решена"

    await query.message.answer(message_text)

    await FeedbackStates.seen_pagination.set()

    paginated = await Pagination('FEEDBACK').paginate(1, 6, dict(is_read=True, status='seen'), user.lang)

    if not paginated['status']:
        await FeedbackStates.process.set()

    await query.message.edit_text(paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == 'back', state=FeedbackStates.one_seen_feedback)
async def back_from_single_seen_feedback_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))
    await FeedbackStates.active_pagination.set()

    paginated = await Pagination('ADVERTISING').paginate(1, 6, dict(is_read=True, status=StatusChoices.SEEN), user.lang)

    if not paginated['status']:
        await FeedbackStates.process.set()

    await query.message.edit_text(paginated['message'], reply_markup=paginated['keyboard'])
