from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from bot.loader import dp
from bot.controllers import user_controller, subject_controller
from bot.models.user import User, StatusChoices
from bot.helpers.formats import introduction_format
from bot.helpers.utils import is_num, translator
from bot.keyboards.keyboard_buttons import option
from bot.keyboards.keyboards import (
    instructor_pages_keyboard,
    student_pages_keyboard,
    language_keyboard,
    send_contact_keyboard,
    type_keyboard,
    subjects_sections_keyboard
)
from bot.states.user import UserStates


@dp.message_handler(commands='start')
async def cmd_start(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if user:
        if user.type == User.TypeChoices.ADMIN:
            await UserStates.process.set()
            return

        message_text = translator('Bosh sahifa', 'Домашняя страница', user.lang)

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

    first_message = translator('Keling tanishamiz', 'Давайте познакомимся', message.text)
    second_message = translator('Ismingiz?', 'Как вас зовут?', message.text)

    async with state.proxy() as data:
        data['user_language'] = message.text

    await UserStates.name.set()

    await message.answer(first_message, reply_markup=ReplyKeyboardRemove())
    await message.answer(second_message)


@dp.message_handler(state=UserStates.name)
async def requesting_user_type_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    if is_num(message.text):
        error_message = translator(
            "Ism sonlardan iborat bo'lmaydi", "Имя не будет состоять из цифр", data['user_language']
        )
        await message.answer(error_message)
        return

    await UserStates.type.set()

    async with state.proxy() as exist_data:
        exist_data['user_name'] = message.text

    message_text = translator(
        "O'zingiz uchun tip tanlang. Siz o'qituvchimisiz yoki o'quvchi",
        "Выберите тип для себя. Вы учитель или ученик?",
        data['user_language']
    )

    await message.answer(message_text, reply_markup=type_keyboard(data['user_language']))


@dp.message_handler(state=UserStates.type)
async def requesting_user_phone_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    if is_num(message.text):
        error_message = translator(
            "Ism sonlardan iborat bo'lmaydi", "Имя не будет состоять из цифр", data['user_language']
        )
        await message.answer(error_message)
        return

    if message.text not in [
        option['types']['uz']['instructor'], option['types']['uz']['student'],
        option['types']['ru']['instructor'], option['types']['ru']['student']
    ]:
        error_message = translator(
            "Tanlash mumkun bo'lgan tiplardan birini tanlang", "Выберите один из доступных типов", data['user_language']
        )
        await message.answer(error_message)
        return

    user_type = User.TypeChoices.INSTRUCTOR \
        if message.text in [option['types']['uz']['instructor'], option['types']['ru']['instructor']] else \
        User.TypeChoices.STUDENT

    async with state.proxy() as data:
        data['user_type'] = user_type

    if user_type == User.TypeChoices.INSTRUCTOR:
        subjects = await subject_controller.get_all(dict(status=StatusChoices.ACTIVE))

        message_text = translator(
            "Qaysi fandan instruktorlik qilasiz", "«Какой предмет вы преподаете»", data['user_language']
        )

        await UserStates.subject.set()

        await message.answer(message_text, reply_markup=subjects_sections_keyboard(subjects, data['user_language']))

        return

    first_message = translator('Telefon raqamingizni ulashing', 'Поделитесь своим контактом', data['user_language'])
    second_message = translator(
        f"Contactingizni jo'natish uchun {option['send']['uz']} ni bosing",
        f"Нажмите {option['send']['ru']} тобы отправить ваш контакт",
        data['user_language']
    )

    await UserStates.phone.set()

    await message.answer(first_message)
    await message.answer(second_message, reply_markup=send_contact_keyboard(data['user_language']))


@dp.message_handler(state=UserStates.subject)
async def requesting_instructor_subject_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    if is_num(message.text):
        error_message = translator(
            "Ism sonlardan iborat bo'lmaydi", "Имя не будет состоять из цифр", data['user_language']
        )
        await message.answer(error_message)
        return

    subject_query = translator(dict(name_uz=message.text), dict(name_ru=message.text), data['user_language'])

    subject = await subject_controller.get_one(subject_query)

    if not subject:
        error_message = translator(
            "Berilgan fanlardan birini tanlang", "Выберите один из предложенных предметов", data['user_language']
        )

        await message.answer(error_message)
        return

    async with state.proxy() as data:
        data['user_subject'] = subject.id

    first_message = translator('Telefon raqamingizni ulashing', 'Поделитесь своим контактом', data['user_language'])
    second_message = translator(
        f"Contactingizni jo'natish uchun {option['send']['uz']} ni bosing",
        f"Нажмите {option['send']['ru']} тобы отправить ваш контакт",
        data['user_language']
    )

    await UserStates.phone.set()

    await message.answer(first_message)
    await message.answer(second_message, reply_markup=send_contact_keyboard(data['user_language']))


@dp.message_handler(content_types=ContentTypes.ANY, state=UserStates.phone)
async def user_creation_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    number, keyboard = 0, []

    if message.text:
        number = message.text
    elif message.contact:
        number = message.contact.phone_number

    if not is_num(number):
        error_message = translator(
            "Telefon raqam sonlardan iborat bo'lishi kerak",
            "Номер телефона должен содержать цифры",
            data['user_language']
        )
        await message.answer(error_message)
        return

    message_text = translator(
        'Registratsiya muvaffaqqiyatli yakunlandi', 'Регистрация успешно завершена', data['user_language']
    )

    user_data = dict(
        telegram_id=message.from_user.id,
        name=data.get('user_name'),
        username=message.from_user.username,
        number=number,
        lang=data.get('user_language'),
        type=data.get('user_type'),
        status=StatusChoices.ACTIVE
    )

    if data.get('user_subject'):
        user_data.update(subject_id=data['user_subject'])

    await user_controller.make(user_data)

    await UserStates.process.set()

    keyboard = instructor_pages_keyboard(data['user_language']) \
        if data['user_type'] == User.TypeChoices.INSTRUCTOR else \
        student_pages_keyboard(data['user_language'])

    await message.answer(message_text, reply_markup=keyboard)

    async with state.proxy() as data:
        del data['user_language']
        del data['user_type']

        if data.get('user_subject'):
            del data['user_subject']

        del data['user_name']
