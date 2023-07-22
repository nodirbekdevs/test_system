from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove
from sqlalchemy import and_
from aiogram.dispatcher import FSMContext
from bot.loader import dp
from bot.controllers import user_controller
from bot.models.user import User, StatusChoices
from bot.helpers.formats import introduction_format
from bot.helpers.utils import is_num
from bot.keyboards.keyboard_buttons import option
from bot.keyboards.keyboards import (
    instructor_pages_keyboard, student_pages_keyboard, language_keyboard, send_contact_keyboard, type_keyboard
)
from bot.states.admin import AdminStates
from bot.states.user import UserStates


@dp.message_handler(commands='start')
async def cmd_start(message: Message, state: FSMContext):
    user = await User.get_user_by_telegram_id(telegram_id=message.from_user.id)

    if user:
        if user.type == User.TypeChoices.ADMIN:
            await UserStates.process.set()
            return

        message_text = 'Bosh sahifa' if user.lang == option['language']['uz'] else 'Домашняя страница'

        if user.type == User.TypeChoices.STUDENT:
            await UserStates.process.set()
            await message.answer(message_text, reply_markup=student_pages_keyboard(user.lang))
            return

        if user.type == User.TypeChoices.INSTRUCTOR:
            await UserStates.process.set()
            await message.answer(message_text, reply_markup=instructor_pages_keyboard(user.lang))
            return

    await UserStates.language.set()

    await message.answer(introduction_format(message.from_user.first_name), reply_markup=language_keyboard())


@dp.message_handler(state=UserStates.language)
async def requesting_user_name_handler(message: Message, state: FSMContext):
    if is_num(message.text) or message.text not in [option['language']['uz'], option['language']['ru']]:
        await message.answer(
            "Iltimos keltirilgan tildan birini tanlang\nПожалуйста, выберите один из перечисленных языков"
        )
        return

    first_message = 'Keling tanishamiz' if message.text == option['language']['uz'] else 'Давайте познакомимся'
    second_message = 'Ismingiz?' if message.text == option['language']['uz'] else 'Как вас зовут?'

    async with state.proxy() as data:
        data['user_language'] = message.text

    await UserStates.name.set()

    await message.answer(first_message, reply_markup=ReplyKeyboardRemove())
    await message.answer(second_message)


@dp.message_handler(state=UserStates.name)
async def requesting_user_type_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    if is_num(message.text):
        error_message = "Ism sonlardan iborat bo'lmaydi" \
            if data['user_language'] == option['language']['uz'] else \
            "Имя не будет состоять из цифр"

        await message.answer(error_message)
        return

    await UserStates.type.set()

    async with state.proxy() as exist_data:
        exist_data['user_name'] = message.text

    message_text = "O'zingiz uchun tip tanlang. Siz o'qituvchimisiz yoki o'quvchi" \
        if data['user_language'] == option['language']['uz'] else \
        "Выберите тип для себя. Вы учитель или ученик?"

    await message.answer(message_text, reply_markup=type_keyboard(data['user_language']))


@dp.message_handler(state=UserStates.type)
async def requesting_user_phone_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    if is_num(message.text):
        error_message = "Ism sonlardan iborat bo'lmaydi" \
            if data['user_language'] == option['language']['uz'] else \
            "Имя не будет состоять из цифр"

        await message.answer(error_message)
        return

    if message.text not in [
        option['types']['uz']['instructor'], option['types']['uz']['student'],
        option['types']['ru']['instructor'], option['types']['ru']['student']
    ]:
        error_message = "Tanlash mumkun bo'lgan tiplardan birini tanlang" \
            if data['user_language'] == option['language']['uz'] else \
            "Выберите один из доступных типов"

        await message.answer(error_message)
        return

    first_message, second_message = "", ""

    if data['user_language'] == option['language']['uz']:
        first_message = 'Telefon raqamingizni ulashing'
        second_message = f"Contactingizni jo'natish uchun {option['send']['uz']} ni bosing"
    elif data['user_language'] == option['language']['ru']:
        first_message = 'Поделитесь своим контактом'
        second_message = f"Нажмите {option['send']['ru']} тобы отправить ваш контакт"

    user_type = User.TypeChoices.INSTRUCTOR \
        if message.text in [option['types']['uz']['instructor'], option['types']['ru']['instructor']] else \
        User.TypeChoices.STUDENT

    async with state.proxy() as data:
        data['user_type'] = user_type

    await UserStates.phone.set()

    await message.answer(first_message)
    await message.answer(second_message, reply_markup=send_contact_keyboard(data['user_language']))


@dp.message_handler(content_types=ContentTypes.ANY, state=UserStates.phone)
async def user_creation_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    phone, keyboard = 0, []

    if message.text:
        phone = message.text
    elif message.contact:
        phone = message.contact.phone_number

    if not is_num(phone):
        error_message = "Telefon raqam sonlardan iborat bo'lishi kerak" \
            if data['user_language'] == option['language']['uz'] else \
            "Номер телефона должен содержать цифры"
        await message.answer(error_message)
        return

    message_text = 'Registratsiya muvaffaqqiyatli yakunlandi' \
        if data['user_language'] == option['language']['uz'] else \
        'Регистрация успешно завершена'

    await user_controller.make(dict(
        telegram_id=message.from_user.id,
        name=data.get('user_name'),
        username=message.from_user.username,
        number=phone,
        lang=data.get('user_language'),
        type=data.get('user_type'),
        status=StatusChoices.ACTIVE
    ))

    await UserStates.process.set()

    keyboard = instructor_pages_keyboard(data['user_language']) \
        if data['user_type'] == User.TypeChoices.INSTRUCTOR else \
        student_pages_keyboard(data['user_language'])

    await message.answer(message_text, reply_markup=keyboard)

    async with state.proxy() as data:
        del data['user_language']
        del data['user_type']
        del data['user_name']
