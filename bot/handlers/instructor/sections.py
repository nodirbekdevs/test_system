from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from deep_translator import GoogleTranslator

from bot.loader import dp
from bot.models.user import User
from bot.models.section import Section
from bot.models.test import Test
from bot.models.subject import Subject
from bot.keyboards.keyboards import instructor_sections_keyboard, one_section_keyboard, subjects_keyboard, confirmation_keyboard, back_keyboard
from bot.filters.is_instructor import IsInstructor
from bot.keyboards.keyboard_buttons import instructor, option
from bot.helpers.utils import Pagination, is_num
from bot.helpers.formats import one_section_format
# from bot.helpers.settings import CORE_ADMINS
from bot.states.section import SectionStates
from bot.states.user import UserStates


@dp.message_handler(
    IsInstructor(),
    text=[instructor['pages']['uz']['sections'], instructor['pages']['ru']['sections']],
    state=UserStates.process
)
async def instructor_sections_handler(message: Message, state: FSMContext):
    user = await User.get_user_by_telegram_id(message.from_user.id)

    message_text = "Bo'limlar sahifasi" if user.lang == option['language']['uz'] else "Страница разделов"

    await SectionStates.process.set()

    await message.answer(message_text, reply_markup=instructor_sections_keyboard(user.lang))


@dp.message_handler(
    IsInstructor(),
    text=[instructor['sections']['uz']['all'], instructor['sections']['ru']['all']],
    state=SectionStates.process
)
async def all_sections_handler(message: Message, state: FSMContext):
    user = await User.get_user_by_telegram_id(message.from_user.id)

    paginated = await Pagination(data_type="SECTION").paginate(query={}, page=1, limit=6, language=user.lang)

    await SectionStates.all_sections.set()

    await message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsInstructor(), lambda query: query.data == "delete", state=SectionStates.all_sections)
async def back_from_all_sections_handler(query: CallbackQuery, state: FSMContext):
    user = await User.get_user_by_telegram_id(query.from_user.id)

    message_text = "Bo'limlar sahifasi" if user.lang == option['language']['uz'] else "Страница разделов"

    await SectionStates.process.set()

    await query.message.edit_text(message_text, reply_markup=instructor_sections_keyboard(user.lang))


@dp.callback_query_handler(
    IsInstructor(),
    lambda query: query.data.startswith("left#sections#") or query.data.startswith("right#sections#"),
    state=SectionStates.all_sections
)
async def pagination_instructor_sections_handler(query: CallbackQuery, state: FSMContext):
    user = await User.get_user_by_telegram_id(query.from_user.id)

    paginated = await Pagination(data_type="SECTION").paginate(query={}, page=1, limit=6, language=user.lang)

    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(
    IsInstructor(), lambda query: query.data.startswith("ssection-"), state=SectionStates.all_sections
)
async def get_instructor_section_handler(query: CallbackQuery, state: FSMContext):
    id = query.data.split("-")[1]

    user = await User.get_user_by_telegram_id(query.from_user.id)

    section = await Section.get_by_id(int(id))

    await SectionStates.one_section.set()

    data = dict(
        user=user.name,
        subject=section.subject_id.name,
        name=section.name,
        description=section.description,
        total_tests=section.total_tests,
        status=section.status,
        created_at=section.created_at
    )

    await query.message.edit_text(
        text=one_section_format(data, user.lang), reply_markup=one_section_keyboard(section.id, user.lang)
    )


@dp.callback_query_handler(IsInstructor(), lambda query: query.data == "back", state=SectionStates.one_section)
async def back_from_get_product_handler(query: CallbackQuery, state: FSMContext):
    user = await User.get_user_by_telegram_id(query.from_user.id)

    paginated = await Pagination(data_type="SECTION").paginate(query={}, page=1, limit=6, language=user.lang)

    await SectionStates.all_sections.set()

    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(
    IsInstructor(), lambda query: query.data.startswith("delete.section."), state=SectionStates.one_section
)
async def delete_product_handler(query: CallbackQuery, state: FSMContext):
    id = query.data.split(".")[2]

    user = await User.get_user_by_telegram_id(query.from_user.id)

    section = await Section.get_by_id(int(id))

    test = await Test.test_is_being_resolved(section.id)

    if not test:
        error_message = "Hozir bo'limni o'chiraolmaysiz. Chunki test hozir yechilyabti" \
            if user.lang == option['language']['uz'] else \
            "Вы не можете удалить раздел сейчас. Поскольку тест в настоящее время решается"

        await query.message.answer(text=error_message)
        return

    deleting = await Section.delete_by_id(section.id)

    if not deleting:
        error_message = "Nimadir noto'g'ri bajarildi. Bir ozdan so'ng harakat qilib ko'ring." \
            if user.lang == option['language']['uz'] else \
            "Что-то пошло не так. Попробуйте позже."

        await query.message.answer(text=error_message)
        return

    paginated = await Pagination(data_type="SECTION").paginate(query={}, page=1, limit=6, language=user.lang)

    await SectionStates.all_sections.set()

    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.message_handler(
    IsInstructor(),
    text=[instructor['sections']['uz']['add'], instructor['sections']['ru']['add']],
    state=SectionStates.process
)
async def requesting_subject_handler(message: Message, state: FSMContext):
    user = await User.get_user_by_telegram_id(message.from_user.id)
    subjects = await Subject.get_all()

    await SectionStates.subject.set()

    message_text = "Qaysi fan uchun bo'lim qo'shmoqchisiz" \
        if user.lang == option['language']['uz'] else \
        "Для какой темы вы хотите добавить раздел"

    await message.answer(text=message_text, reply_markup=subjects_keyboard(subjects, user.lang, 3))


@dp.message_handler(IsInstructor(), state=SectionStates.subject)
async def requesting_name_handler(message: Message, state: FSMContext):
    user = await User.get_user_by_telegram_id(message.from_user.id)

    if is_num(message.text):
        error_message = "Raqam jo'natmang!" if user.lang == option['language']['uz'] else "Не присылайте номер!"
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = "Bekor qilindi" if user['lang'] == option['language']['uz'] else "Отменено"

        await message.answer(error_message)
        await instructor_sections_handler(message, state)
        return

    subject_checking = await Subject.check_by_name(message.text)

    if not subject_checking:
        error_message = "Berilgan fanlardan birini tanlang" \
            if user.lang == option['language']['uz'] else \
            "Выберите один из предложенных предметов"

        await message.answer(error_message)
        return

    async with state.proxy() as data:
        data['section_subject'] = message.text

    await SectionStates.name.set()

    message_text = "Bo'lim uchun nom yozing" if user.lang == option['language']['uz'] else "Введите название раздела"

    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(state=SectionStates.name)
async def requesting_description_handler(message: Message, state: FSMContext):
    user = await User.get_user_by_telegram_id(message.from_user.id)

    if is_num(message.text):
        error_message = "Raqam jo'natmang!" if user.lang == option['language']['uz'] else "Не присылайте номер!"
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = "Bekor qilindi" if user['lang'] == option['language']['uz'] else "Отменено"

        await message.answer(error_message)
        await instructor_sections_handler(message, state)
        return

    section_checking = await Section.check_by_name(message.text)

    if section_checking:
        error_message = "Bu nom bilan bo'lim mavjud" \
            if user.lang == option['language']['uz'] else \
            "Есть раздел с таким названием"

        await message.answer(error_message)
        return

    async with state.proxy() as data:
        data['section_name'] = message.text

    await SectionStates.description.set()

    message_text = "Bo'lim uchun tavsif yozing" if user.lang == option['language']['uz'] else "Введите описание раздела"

    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(state=SectionStates.description)
async def checking_section_creation_handler(message: Message, state: FSMContext):
    user = await User.get_user_by_telegram_id(message.from_user.id)

    if is_num(message.text):
        error_message = "Raqam jo'natmang!" if user.lang == option['language']['uz'] else "Не присылайте номер!"
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = "Bekor qilindi" if user['lang'] == option['language']['uz'] else "Отменено"

        await message.answer(error_message)
        await instructor_sections_handler(message, state)
        return

    async with state.proxy() as data:
        data['section_description'] = message.text

    state_data = await state.get_data()

    await SectionStates.checking.set()

    dope = dict(
        subject=state_data.get('section_subject'),
        name=state_data.get('section_name'),
        description=message.text
    )

    await message.answer(
        one_section_format(data=dope, language=user.lang, is_editing=True), reply_markup=confirmation_keyboard(user.lang)
    )


@dp.message_handler(IsInstructor(), state=SectionStates.checking)
async def section_creation_handler(message: Message, state: FSMContext):
    user = await User.get_user_by_telegram_id(message.from_user.id)

    if is_num(message.text):
        error_message = "Raqam jo'natmang!" if user.lang == option['language']['uz'] else "Не присылайте номер!"
        await message.answer(error_message)
        return

    if message.text in [option['not_to_confirmation']['uz'], option['not_to_confirmation']['ru']]:
        await SectionStates.process.set()
        error_message = "Bo'lim muvaffaqqiyatli qo'shilmadi!" \
            if user.lang == option['language']['uz'] else \
            "Раздел не был успешно добавлен!"
        await message.answer(error_message, reply_markup=instructor_sections_keyboard(user.lang))
        return

    if message.text not in [option['confirmation']['uz'], option['confirmation']['ru']]:
        error_message = "Bosishingiz kerak bo'lgan variantlardan birini jo'nating" \
            if user.lang == option['language']['uz'] else \
            "Отправьте один из вариантов, который вам нужно нажать"
        await message.answer(error_message)
        return

    await SectionStates.process.set()

    data = await state.get_data()

    subject, name, description = data.get('section_subject'), data.get('section_name'), data.get('section_description')

    subject = await Subject.check_by_name(name)

    section = await Section.create(
        user_id=user.id,
        subject_id=subject.id,
        name=name,
        description=description
    )

    dope = dict(
        user=user.name,
        subject=subject,
        name=name,
        description=description,
        total_tests=section.total_tests,
        status=section.status,
        created_at=section.created_at
    )

    async with state.proxy() as data:
        del data['section_subject']
        del data['section_name']
        del data['section_description']

    message_text = "Bo'lim muvaffaqqiyatli qo'shildi" if user.lang == option['language']['uz'] else "Раздел успешно добавлен"

    await message.answer(one_section_format(dope, user.lang))

    await message.answer(message_text, reply_markup=instructor_sections_keyboard(user.lang))