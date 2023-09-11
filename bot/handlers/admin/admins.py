from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.loader import dp
from bot.filters.is_admin import IsAdmin
from bot.controllers import user_controller
from bot.models.user import User
from bot.keyboards.keyboards import admin_keyboard, one_admin_keyboard, back_keyboard
from bot.keyboards.keyboard_buttons import admin, option
from bot.helpers.utils import Pagination, is_num, translator
from bot.helpers.config import ADMIN
from bot.helpers.formats import user_format, back_format
from bot.states.admin import AdminStates
from bot.states.user import UserStates


@dp.message_handler(
    IsAdmin(), text=[admin['pages']['uz']['admins'], admin['pages']['ru']['admins']], state=UserStates.process
)
async def admin_admins_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.chat.id))

    message_text = translator("Adminlar sahifasi", "Страница администратораов", user.lang)

    await AdminStates.process.set()

    await message.answer(message_text, reply_markup=admin_keyboard(ADMIN, user.lang))


@dp.message_handler(
    IsAdmin(), text=[admin['admins']['uz']['all'], admin['admins']['ru']['all']], state=AdminStates.process
)
async def all_admins_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    paginated = await Pagination("ADMIN").paginate(1, 6, dict(type=User.TypeChoices.ADMIN), user.lang)

    if paginated['status']:
        await AdminStates.all_admins.set()

    await message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == "delete", state=AdminStates.all_admins)
async def back_from_all_admins_handler(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await admin_admins_handler(query.message, state)


@dp.callback_query_handler(
    IsAdmin(),
    lambda query: query.data.startswith("left#admins#") or query.data.startswith("right#admins#"),
    state=AdminStates.all_admins
)
async def pagination_admins_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    page = int(query.data.split("#")[2])

    paginated = await Pagination("ADMIN").paginate(page, 6, dict(type=User.TypeChoices.ADMIN), user.lang)

    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data.startswith("sadmin-"), state=AdminStates.all_admins)
async def get_admin_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    id = int(query.data.split("-")[1])

    selected_admin = await user_controller.get_one(dict(id=id))

    await AdminStates.one_admin.set()

    await query.message.edit_text(
        text=user_format(selected_admin, user.lang), reply_markup=one_admin_keyboard(id, user.lang)
    )


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == "back", state=AdminStates.one_admin)
async def back_from_get_admin_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    paginated = await Pagination("ADMIN").paginate(1, 6, dict(type=User.TypeChoices.ADMIN), user.lang)

    await AdminStates.all_admins.set()

    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data.startswith("delete.admin."), state=AdminStates.one_admin)
async def delete_admin_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    id = int(query.data.split(".")[2])

    await user_controller.delete(dict(id=id))

    paginated = await Pagination("ADMIN").paginate(1, 6, dict(type=User.TypeChoices.ADMIN), user.lang)

    if not paginated['status']:
        await AdminStates.process.set()
        await query.message.delete()
        await query.message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])
    elif paginated['status']:
        await AdminStates.all_admins.set()
        await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.message_handler(
    IsAdmin(), text=[admin['admins']['uz']['add'], admin['admins']['ru']['add']], state=AdminStates.process
)
async def add_admin_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    await AdminStates.add.set()

    message_text = translator(
        "Yangi adminning telegram_id raqamini yuboring", "Отправьте telegram_id нового админа", user.lang
    )

    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsAdmin(), state=AdminStates.add)
async def add_admin_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = back_format(user.lang)
        await message.answer(error_message)
        await admin_admins_handler(message, state)
        return

    if not is_num(message.text):
        error_message = translator(
            "Iltimos to'g'ri telegram_id yuboring", "Пожалуйста, отправьте правильный telegram_id", user.lang
        )
        await message.answer(error_message)
        return

    if message.from_user.id == int(message.text):
        error_message = translator(
            "Boshqa adminning telegram idsini yuboring. Bu telegram id sizga tegishli.",
            "Отправьте telegrma id другого админа. Это telegram id пренадлежит вам.",
            user.lang
        )
        await message.answer(error_message)
        return

    selected_admin = await user_controller.get_one(dict(telegram_id=int(message.text)))

    message_text = translator("Yangi admin qo'shildi", "Добавлен новый админ", user.lang)

    if selected_admin:
        await selected_admin.update(type=User.TypeChoices.ADMIN).apply()
        new_admin_message = translator(
            "Siz admin sifatida botdan foydalanishga muvaffaqiyatli qo‘shildingiz.\n /start tugmasini bosing.",
            "Нажмите Вы успешно присоединились, чтобы использовать бота в качестве администратора.\n /start.",
            selected_admin.lang
        )
        await dp.bot.send_message(chat_id=selected_admin.telegram_id, text=new_admin_message)
        await message.answer(message_text, reply_markup=admin_keyboard(ADMIN, user.lang))
        return

    try:
        admin = await dp.bot.get_chat(chat_id=int(message.text))
    except:
        error_message = translator(
            "telegram_id noto'g'ri jo'natilgan yoki yangi admin botga start bosmagan",
            "Неправильно отправлен telegram_id или новый админ не нажал старт на боте",
            user.lang
        )
        await message.answer(error_message)
        return

    admin_lang = option['language']['uz'] if user.lang == option['language']['uz'] else option['language']['ru']

    admin_data = dict(
        telegram_id=admin['id'],
        name=admin['first_name'],
        username=admin['username'],
        lang=admin_lang,
        type=User.TypeChoices.ADMIN
    )

    await AdminStates.process.set()

    new_admin = await user_controller.make(admin_data)

    new_admin_message = translator(
        "Siz admin sifatida botdan foydalanishga muvaffaqiyatli qo‘shildingiz.\n /start tugmasini bosing.",
        "Нажмите Вы успешно присоединились, чтобы использовать бота в качестве администратора.\n /start.",
        new_admin.lang
    )

    await dp.bot.send_message(chat_id=admin['id'], text=new_admin_message)

    await message.delete()

    await message.answer(message_text, reply_markup=admin_keyboard(ADMIN, user.lang))
