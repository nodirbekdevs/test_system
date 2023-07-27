from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.loader import dp, bot
from bot.filters.is_admin import IsAdmin
from bot.helpers.config import INSTRUCTOR
from bot.controllers import user_controller
from bot.models.user import User
from bot.keyboards.keyboards import  admin_instructors_keyboard, one_admin_instructor_keyboard, back_keyboard
from bot.keyboards.keyboard_buttons import admin, option
from bot.helpers.utils import Pagination, is_num
from bot.helpers.formats import user_format
from bot.states.instructors import InstructorStates
from bot.states.user import UserStates


@dp.message_handler(
    IsAdmin(), text=[admin['pages']['uz']['instructors'], admin['pages']['ru']['instructors']], state=UserStates.process
)
async def admin_instructors_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    message_text = "Instructorlar sahifasi" if user.lang == option['language']['uz'] else "Страница инструкторов"

    await InstructorStates.process.set()

    await message.answer(message_text, reply_markup=admin_instructors_keyboard(user.lang))


@dp.message_handler(
    IsAdmin(), text=[admin['instructors']['uz']['all'], admin['instructors']['ru']['all']], state=InstructorStates.process
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

    paginated = await Pagination("INSTRUCTOR").paginate(1, 6, dict(type=User.TypeChoices.INSTRUCTOR), user.lang)

    await InstructorStates.all_instructors.set()

    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


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


@dp.message_handler(
    IsAdmin(), text=[admin['instructors']['uz']['add'], admin['instructors']['ru']['add']], state=InstructorStates.process
)
async def add_instructor_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    await InstructorStates.add.set()

    message_text = "Yangi instructorning telegram_id raqamini yuboring" \
        if user.lang == option['language']['uz'] else \
        "Отправьте telegram_id нового инструктора"

    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsAdmin(), state=InstructorStates.add)
async def creating_instructor_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = "Bekor qilindi" if user.lang == option['language']['uz'] else "Отменено"
        await message.answer(error_message)
        await admin_instructors_handler(message, state)
        return

    if not is_num(message.text):
        message_text = "Iltimos to'g'ri telegram_id yuboring" \
            if user.lang == option['language']['uz'] else \
            "Пожалуйста, отправьте правильный telegram_id"

        await message.answer(message_text)
        return

    if message.from_user.id == int(message.text):
        await message.answer(
            text="Отправьте telegrma id другого инструктора. Это telegram id пренадлежит вам."
        )
        return

    selected_admin = await user_controller.get_one(dict(telegram_id=int(message.text)))

    if selected_admin:
        message_text = "Yangi instructor qo'shildi" if user.lang == option['language']['uz'] else "Добавлен новый инструктор"

        await selected_admin.update(type=User.TypeChoices.ADMIN).apply()
        await InstructorStates.process.set()
        await message.answer(message_text, reply_markup=admin_instructors_keyboard(user.lang))
        return

    try:
        admin = await bot.get_chat(chat_id=int(message.text))
    except:
        error_message = "telegram_id noto'g'ri jo'natilgan yoki yangi instructor botga start bosmagan" \
            if user.lang == option['language']['uz'] else \
            "Неправильно отправлен telegram_id или новый инструктор не нажал старт на боте"

        await message.answer(error_message)
        return

    admin_lang = option['language']['uz'] if user.lang == option['language']['uz'] else option['language']['ru']

    admin_data = dict(
        telegram_id=admin['id'],
        name=admin['first_name'],
        username=admin['username'],
        lang=admin_lang,
        type=User.TypeChoices.INSTRUCTOR
    )

    await user_controller.make(admin_data)

    await InstructorStates.process.set()

    await dp.bot.send_message(
        chat_id=admin['id'], text="Вы успешно добавлены на пользования бота на роле инструктора.\n Нажмите /start"
    )

    await message.delete()

    message_text = "Yangi instructor qo'shildi" if user.lang == option['language']['uz'] else "Новый инструктор добален"

    await message.answer(message_text, reply_markup=admin_instructors_keyboard(user.lang))
