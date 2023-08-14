from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from deep_translator import GoogleTranslator

from bot.loader import dp
from bot.controllers import user_controller, section_controller, test_controller, subject_controller
from bot.models.user import User
from bot.models.section import Section
from bot.keyboards.keyboards import instructor_keyboard, one_instructor_keyboard, confirmation_keyboard, back_keyboard
from bot.filters.is_instructor import IsInstructor
from bot.keyboards.keyboard_buttons import instructor, option
from bot.helpers.utils import Pagination, is_num, translator, translate_text
from bot.helpers.config import SECTION
from bot.helpers.formats import section_format
from bot.states.section import SectionStates
from bot.states.user import UserStates


@dp.message_handler(
    IsInstructor(),
    text=[instructor['pages']['uz']['sections'], instructor['pages']['ru']['sections']],
    state=UserStates.process
)
async def instructor_sections_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.chat.id))

    message_text = translator("Bo'limlar sahifasi", "Страница разделов", user.lang)

    await SectionStates.process.set()

    await message.answer(message_text, reply_markup=instructor_keyboard(SECTION, user.lang))


@dp.message_handler(
    IsInstructor(),
    text=[instructor['sections']['uz']['all'], instructor['sections']['ru']['all']],
    state=SectionStates.process
)
async def all_sections_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    paginated = await Pagination(data_type="SECTION").paginate(1, 6, dict(user_id=user.id), user.lang)

    if paginated['status']:
        await SectionStates.all_sections.set()

    await message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsInstructor(), lambda query: query.data == "delete", state=SectionStates.all_sections)
async def back_from_all_sections_handler(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await instructor_sections_handler(query.message, state)


@dp.callback_query_handler(
    IsInstructor(),
    lambda query: query.data.startswith("left#sections#") or query.data.startswith("right#sections#"),
    state=SectionStates.all_sections
)
async def pagination_instructor_sections_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    paginated = await Pagination(data_type="SECTION").paginate(1, 6, dict(user_id=user.id), user.lang)

    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(
    IsInstructor(), lambda query: query.data.startswith("ssection-"), state=SectionStates.all_sections
)
async def get_instructor_section_handler(query: CallbackQuery, state: FSMContext):
    id = int(query.data.split("-")[1])

    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    section = await section_controller.get_one(dict(id=id))

    subject = await subject_controller.get_one(dict(id=section.subject_id))

    await SectionStates.one_section.set()

    data = dict(
        user=user.name,
        subject=translator(subject.name_uz, subject.name_ru, user.lang),
        name=translator(section.name_uz, section.name_ru, user.lang),
        description=translator(section.description_uz, section.description_ru, user.lang),
        total_tests=section.total_tests,
        status=section.status,
        created_at=section.created_at
    )

    await query.message.edit_text(
        text=section_format(data, user.lang), reply_markup=one_instructor_keyboard(section.id, SECTION, user.lang)
    )


@dp.callback_query_handler(IsInstructor(), lambda query: query.data == "back", state=SectionStates.one_section)
async def back_from_get_section_handler(query: CallbackQuery, state: FSMContext):
    user = await User.get_user_by_telegram_id(query.from_user.id)

    paginated = await Pagination(data_type="SECTION").paginate(1, 6, dict(user_id=user.id), user.lang)

    await SectionStates.all_sections.set()

    if not paginated['status']:
        await SectionStates.process.set()

    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(
    IsInstructor(), lambda query: query.data.startswith("delete.section."), state=SectionStates.one_section
)
async def delete_section_handler(query: CallbackQuery, state: FSMContext):
    id = int(query.data.split(".")[2])

    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    section = await section_controller.get_one(dict(id=id))

    tests = await test_controller.get_all(dict(section_id=section.id))

    if tests:
        for test in tests:
            if test.is_testing:
                error_message = translator(
                    "Hozir bo'limni o'chiraolmaysiz. Chunki test hozir yechilyabti",
                    "Вы не можете удалить раздел сейчас. Поскольку тест в настоящее время решается",
                    user.lang
                )
                await query.message.answer(text=error_message)
                return

    deleting = await section_controller.delete(dict(id=section.id))

    if not deleting:
        error_message = translator(
            "Nimadir noto'g'ri bajarildi. Bir ozdan so'ng harakat qilib ko'ring.",
            "Что-то пошло не так. Попробуйте позже.",
            user.lang
        )

        await query.message.answer(text=error_message)
        return

    paginated = await Pagination(data_type="SECTION").paginate(1, 6, dict(user_id=user.id), user.lang)

    if paginated['status']:
        await SectionStates.all_sections.set()
        await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])
    elif not paginated['status']:
        await SectionStates.process.set()
        await query.message.delete()
        await query.message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.message_handler(
    IsInstructor(),
    text=[instructor['sections']['uz']['add'], instructor['sections']['ru']['add']],
    state=SectionStates.process
)
async def requesting_subject_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    await SectionStates.name.set()

    message_text = translator("Bo'lim uchun nom yozing", "Введите название раздела", user.lang)
    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


# @dp.message_handler(IsInstructor(), state=SectionStates.subject)
# async def requesting_name_handler(message: Message, state: FSMContext):
#     user = await user_controller.get_one(dict(telegram_id=message.from_user.id))
#
#     if is_num(message.text):
#         error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
#         await message.answer(error_message)
#         return
#
#     if message.text in [option['back']['uz'], option['back']['ru']]:
#         error_message = translator("Bekor qilindi", "Отменено", user.lang)
#         await message.answer(error_message, reply_markup=instructor_keyboard(SECTION, user.lang))
#         return
#
#     subject_query = translator(dict(name_uz=message.text), dict(name_ru=message.text), user.lang)
#
#     subject_checking = await subject_controller.get_one(subject_query)
#
#     if not subject_checking:
#         error_message = translator(
#             "Berilgan fanlardan birini tanlang",  "Выберите один из предложенных предметов", user.lang
#         )
#
#         await message.answer(error_message)
#         return
#
#     async with state.proxy() as data:
#         data['section_subject'] = message.text
#
#     await SectionStates.name.set()
#
#     message_text = translator("Bo'lim uchun nom yozing", "Введите название раздела", user.lang)
#     await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsInstructor(), state=SectionStates.name)
async def requesting_description_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)
        await message.answer(error_message, reply_markup=instructor_keyboard(SECTION, user.lang))
        return

    section_query = translator(
        dict(user_id=user.id, name_uz=message.text), dict(user_id=user.id, name_ru=message.text), user.lang
    )

    section_checking = await section_controller.get_one(section_query)

    if section_checking:
        error_message = translator("Bu nom bilan bo'lim mavjud", "Есть раздел с таким названием", user.lang)

        await message.answer(error_message)
        return

    async with state.proxy() as data:
        data['section_name'] = message.text

    await SectionStates.description.set()

    message_text = translator("Bo'lim uchun tavsif yozing", "Введите описание раздела", user.lang)

    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsInstructor(), state=SectionStates.description)
async def checking_section_creation_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)
        await SectionStates.process.set()
        await message.answer(error_message, reply_markup=instructor_keyboard(SECTION, user.lang))
        return

    async with state.proxy() as data:
        data['section_description'] = message.text

    state_data = await state.get_data()

    await SectionStates.checking.set()

    subject = await subject_controller.get_one(dict(id=user.subject_id))

    subject_name = translator(subject.name_uz, subject.name_ru, user.lang)

    dope = dict(
        subject=subject_name,
        name=state_data.get('section_name'),
        description=message.text
    )

    await message.answer(
        section_format(dope, user.lang, True), reply_markup=confirmation_keyboard(user.lang)
    )


@dp.message_handler(IsInstructor(), state=SectionStates.checking)
async def section_creation_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text in [option['not_to_confirmation']['uz'], option['not_to_confirmation']['ru']]:
        await SectionStates.process.set()
        error_message = translator("Bo'lim muvaffaqqiyatli qo'shilmadi!", "Раздел не был успешно добавлен!", user.lang)
        await message.answer(error_message, reply_markup=instructor_keyboard(SECTION, user.lang))
        return

    if message.text not in [
        option['confirmation']['uz'], option['confirmation']['ru'],
        option['not_to_confirmation']['uz'], option['not_to_confirmation']['ru']
    ]:
        error_message = translator(
            "Bosishingiz kerak bo'lgan variantlardan birini jo'nating",
            "Отправьте один из вариантов, который вам нужно нажать",
            user.lang
        )
        await message.answer(error_message)
        return

    await SectionStates.process.set()

    data = await state.get_data()

    name, description = data.get('section_name'), data.get('section_description')

    translator_language = translator('ru', 'uz', user.lang)

    translated = GoogleTranslator(source='auto', target=translator_language)

    translated_section_name = await translate_text(translated, name)
    translated_section_description = await translate_text(translated, description)

    name_uz, name_ru, description_uz, description_ru = '', '', '', ''

    if user.lang == option['language']['uz']:
        name_uz = name
        name_ru = translated_section_name
        description_uz = description
        description_ru = translated_section_description
    elif user.lang == option['language']['ru']:
        name_uz = translated_section_name
        name_ru = name
        description_uz = translated_section_description
        description_ru = description

    await Section.create(
        user_id=user.id,
        subject_id=user.subject_id,
        name_uz=name_uz,
        name_ru=name_ru,
        description_uz=description_uz,
        description_ru=description_ru
    )

    # dope = dict(
    #     user=user.name,
    #     subject=translator(subject.name_uz, subject.name_ru, user.lang),
    #     name=translator(section.name_uz, section.name_ru, user.lang),
    #     description=translator(section.description_uz, section.description_ru, user.lang),
    #     total_tests=section.total_tests,
    #     status=section.status,
    #     created_at=section.created_at
    # )

    async with state.proxy() as data:
        del data['section_name']
        del data['section_description']

    message_text = translator("Bo'lim muvaffaqqiyatli qo'shildi", "Раздел успешно добавлен", user.lang)

    # await message.answer(section_format(dope, user.lang))

    await message.answer(message_text, reply_markup=instructor_keyboard(SECTION, user.lang))