from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.loader import dp
from bot.filters.is_admin_and_instructor import IsAdminAndInstructor
from bot.filters.is_admin import IsAdmin
from bot.helpers.config import INSTRUCTOR
from bot.controllers import user_controller
from bot.models.user import User
from bot.keyboards.keyboards import admin_keyboard, one_admin_keyboard, back_keyboard
from bot.keyboards.keyboard_buttons import admin, option
from bot.helpers.utils import Pagination, translator
from bot.helpers.formats import user_format
from bot.helpers.config import STUDENT
from bot.states.students import StudentStates
from bot.states.user import UserStates


@dp.message_handler(
    IsAdmin(), text=[admin['pages']['uz']['students'], admin['pages']['ru']['students']], state=UserStates.process
)
async def admin_students_handler(message: Message, state: FSMContext):
    paginated = await Pagination("STUDENT").paginate(1, 6, dict(type=User.TypeChoices.STUDENT), user.lang)

    if paginated['status']:
        await StudentStates.all_students.set()

    await message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.message_handler(
    IsAdmin(), text=[admin['instructors']['uz']['all'], admin['instructors']['ru']['all']], state=StudentStates.process
)
async def all_instructors_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    paginated = await Pagination("INSTRUCTORS").paginate(1, 6, dict(type=User.TypeChoices.INSTRUCTOR), user.lang)

    if paginated['status']:
        await InstructorStates.all_instructors.set()

    await message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == "delete", state=InstructorStates.all_instructors)
async def back_from_all_instructors_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    message_text = "Instructorlar sahifasi" if user.lang == option['language']['uz'] else "Страница инструкторов"

    await InstructorStates.process.set()

    await query.message.delete()

    await query.message.answer(text=message_text, reply_markup=admin_instructors_keyboard(user.lang))


@dp.callback_query_handler(
    IsAdmin(),
    lambda query: query.data.startswith("left#instructors#") or query.data.startswith("right#instructors#"),
    state=InstructorStates.all_instructors
)
async def pagination_instructors_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    page = int(query.data.split("#")[2])

    paginated = await Pagination("INSTRUCTORS").paginate(page, 6, dict(type=User.TypeChoices.INSTRUCTOR), user.lang)

    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data.startswith("sins_"), state=InstructorStates.all_instructors)
async def get_instructors_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    id = int(query.data.split("_")[1])

    selected_instructor = await user_controller.get_one(dict(id=id))

    await InstructorStates.one_instructor.set()

    await query.message.edit_text(
        text=user_format(selected_instructor, user.lang),
        reply_markup=one_admin_instructor_keyboard(id, INSTRUCTOR)
    )


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == "back", state=InstructorStates.one_instructor)
async def back_from_get_instructor_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    paginated = await Pagination("INSTRUCTORS").paginate(1, 6, dict(type=User.TypeChoices.INSTRUCTOR), user.lang)

    if paginated['status']:
        await InstructorStates.all_instructors.set()
        await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])
    else:
        await InstructorStates.process.set()
        await query.message.delete()
        await query.message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data.startswith("delete.instructor."), state=InstructorStates.one_instructor)
async def delete_instructor_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    id = int(query.data.split(".")[2])

    await user_controller.delete(dict(id=id))

    paginated = await Pagination("INSTRUCTORS").paginate(1, 6, dict(type=User.TypeChoices.INSTRUCTOR), user.lang)

    if not paginated['status']:
        await InstructorStates.process.set()
        await query.message.delete()
        await query.message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])
    elif paginated['status']:
        await InstructorStates.all_instructors.set()
        await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])
