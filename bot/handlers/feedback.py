from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from bot.loader import dp
from bot.filters.is_not_admin import IsNotAdmin
from bot.controllers import user_controller, feedback_controller
from bot.models.feedback import StatusChoices
from bot.helpers.formats import feedback_all_format
from bot.helpers.utils import translator
from bot.keyboards.keyboard_buttons import option, instructor, all
from bot.keyboards.keyboards import student_instructor_feedback_keyboard, feedback_keyboard, back_keyboard
from bot.states.feedback import FeedbackStates
from bot.states.user import UserStates


@dp.message_handler(
    IsNotAdmin(),
    text=[instructor['pages']['uz']['feedback'], instructor['pages']['ru']['feedback']],
    state=UserStates.process
)
async def student_instructor_feedback_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.chat.id))

    message_text = translator("Izohlar bo'limi", "Страница комментарии", user.lang)

    await FeedbackStates.process.set()

    await message.answer(message_text, reply_markup=student_instructor_feedback_keyboard(user.lang))


@dp.message_handler(
    IsNotAdmin(),
    text=[all['feedback']['uz']['add'], all['feedback']['ru']['add']],
    state=FeedbackStates.process
)
async def add_student_instructor_feedback_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    message_text = translator("Biz haqimizda nima deb o'ylaysiz", "Что вы думаете о нас", user.lang)

    await FeedbackStates.mark.set()

    await message.answer(message_text, reply_markup=feedback_keyboard(user.lang))


@dp.message_handler(IsNotAdmin(), state=FeedbackStates.mark)
async def requesting_student_instructor_feedback_reason_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)

        await message.answer(error_message)
        await student_instructor_feedback_handler(message, state)
        return

    if message.text not in [
        option['feedback']['uz']['good'], option['feedback']['uz']['bad'],
        option['feedback']['ru']['good'], option['feedback']['ru']['bad']
    ]:
        error_message = translator(
            "Sizga berilgan 2 tugmadan birini bosing", "Нажмите одну из двух кнопок, данных вам", user.lang
        )

        await message.answer(error_message)
        return

    message_text = translator(
        f"Nega {message.text} ligini sababini yozing", f"Напишите причину, по которой {message.text}", user.lang
    )

    async with state.proxy() as data:
        data['user_feedback_mark'] = message.text

    await FeedbackStates.reason.set()

    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsNotAdmin(), state=FeedbackStates.reason)
async def creation_student_instructor_feedback_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)

        await message.answer(error_message)
        await student_instructor_feedback_handler(message, state)
        return

    message_text = translator("Izohingiz muvaffaqiyatli qoldirildi", "Ваш комментарий успешно отправлен.", user.lang)

    await feedback_controller.make(dict(user_id=user.id, mark=data['user_feedback_mark'], reason=message.text))

    await FeedbackStates.process.set()

    await message.answer(message_text, reply_markup=student_instructor_feedback_keyboard(user.lang))


@dp.message_handler(
    IsNotAdmin(),
    text=[all['feedback']['uz']['my_feedback'], all['feedback']['ru']['my_feedback']],
    state=FeedbackStates.process
)
async def all_student_instructor_feedback_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    count = await feedback_controller.count(dict(user_id=user.id))

    if count < 0:
        error_message = translator("Hozircha siz izoh qoldirmagansiz", "Вы еще не оставили комментарий", user.lang)
        await message.answer(error_message)
        return

    active = await feedback_controller.count(dict(user_id=user.id, status=StatusChoices.ACTIVE))
    seen = await feedback_controller.count(dict(user_id=user.id, status=StatusChoices.SEEN))
    done = await feedback_controller.count(dict(user_id=user.id, status=StatusChoices.DONE))

    feedback_data = dict(count=count, active=active, seen=seen, done=done)

    await message.answer(
        feedback_all_format(feedback_data, user.lang),
        reply_markup=student_instructor_feedback_keyboard(user.lang)
    )
