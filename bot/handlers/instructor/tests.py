import aiofiles
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentTypes

from deep_translator import GoogleTranslator
from os import mkdir
from os.path import join, abspath, dirname, exists
from asyncio import to_thread

from bot.loader import dp
from bot.controllers import user_controller, section_controller, test_controller, subject_controller
from bot.models.user import User
from bot.models.test import StatusChoices
from bot.keyboards.keyboards import instructor_keyboard, one_instructor_keyboard, subjects_sections_keyboard, \
    confirmation_keyboard, next_keyboard, back_keyboard
from bot.filters.is_instructor import IsInstructor
from bot.keyboards.keyboard_buttons import instructor, option
from bot.helpers.utils import Pagination, is_num, translator
from bot.helpers.formats import test_format
from bot.helpers.config import TEST
from bot.states.test import TestStates
from bot.states.user import UserStates


@dp.message_handler(
    IsInstructor(),
    text=[instructor['pages']['uz']['tests'], instructor['pages']['ru']['tests']],
    state=UserStates.process
)
async def instructor_tests_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.chat.id))

    message_text = translator("Testlar sahifasi", "Страница тестов", user.lang)

    await TestStates.process.set()

    await message.answer(message_text, reply_markup=instructor_keyboard(TEST, user.lang))


@dp.message_handler(
    IsInstructor(),
    text=[instructor['tests']['uz']['all'], instructor['tests']['ru']['all']],
    state=TestStates.process
)
async def all_tests_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    paginated = await Pagination(data_type="TEST").paginate(
        1, 6, dict(user_id=user.id, status=StatusChoices.ACTIVE), user.lang, ['subject_id', 'section_id']
    )

    if paginated['status']:
        await TestStates.all_tests.set()

    await message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsInstructor(), lambda query: query.data == "delete", state=TestStates.all_tests)
async def back_from_all_tests_handler(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await instructor_tests_handler(query.message, state)


@dp.callback_query_handler(
    IsInstructor(),
    lambda query: query.data.startswith("left#tests#") or query.data.startswith("right#tests#"),
    state=TestStates.all_tests
)
async def pagination_instructor_tests_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    paginated = await Pagination(data_type="TEST").paginate(
        1, 6, dict(user_id=user.id, status=StatusChoices.ACTIVE), user.lang, ['subject_id', 'section_id']
    )

    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(
    IsInstructor(), lambda query: query.data.startswith("stest-"), state=TestStates.all_tests
)
async def get_instructor_test_handler(query: CallbackQuery, state: FSMContext):
    id = int(query.data.split("-")[1])

    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    test = await test_controller.get_one(dict(id=id))

    subject = await subject_controller.get_one(dict(id=test.subject_id))
    section = await section_controller.get_one(dict(id=test.section_id))

    await TestStates.one_test.set()

    data = dict(
        owner=user.name,
        subject=translator(subject.name_uz, subject.name_ru, user.lang),
        section=translator(section.name_uz, section.name_ru, user.lang),
        question=translator(test.question_uz, test.question_ru, user.lang),
        variants=translator(test.variants_uz, test.variants_ru, user.lang),
        correct_answer=translator(test.correct_answer_uz, test.correct_answer_ru, user.lang),
        status=test.status,
        created_at=test.created_at
    )

    await query.message.edit_text(
        text=test_format(data, user.lang), reply_markup=one_instructor_keyboard(test.id, TEST, user.lang)
    )


@dp.callback_query_handler(IsInstructor(), lambda query: query.data == "back", state=TestStates.one_test)
async def back_from_get_test_handler(query: CallbackQuery, state: FSMContext):
    user = await User.get_user_by_telegram_id(query.from_user.id)

    paginated = await Pagination(data_type="TEST").paginate(
        1, 6, dict(user_id=user.id, status=StatusChoices.ACTIVE), user.lang, ['subject_id', 'section_id']
    )

    await TestStates.all_tests.set()

    if not paginated['status']:
        await TestStates.process.set()

    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(
    IsInstructor(), lambda query: query.data.startswith("delete.test."), state=TestStates.one_test
)
async def delete_test_handler(query: CallbackQuery, state: FSMContext):
    id = int(query.data.split(".")[2])

    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    test = await test_controller.get_one(dict(id=id))

    if test.is_testing:
        error_message = translator(
            "Hozir testni o'chiraolmaysiz chunki test yechilyabdi.",
            "Вы не можете удалить тест сейчас, потому что тест решается.",
            user.lang
        )
        await query.message.answer(text=error_message)
        return

    deleting = await test_controller.delete(dict(id=test.id))

    if not deleting:
        error_message = translator(
            "Nimadir noto'g'ri bajarildi. Bir ozdan so'ng harakat qilib ko'ring.",
            "Что-то пошло не так. Попробуйте позже.",
            user.lang
        )
        await query.message.answer(text=error_message)
        return

    paginated = await Pagination(data_type="TEST").paginate(
        1, 6, dict(user_id=user.id, status=StatusChoices.ACTIVE), user.lang, ['subject_id', 'section_id']
    )

    if paginated['status']:
        await TestStates.all_tests.set()
        await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])
    elif not paginated['status']:
        await TestStates.process.set()
        await query.message.delete()
        await query.message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.message_handler(
    IsInstructor(),
    text=[instructor['tests']['uz']['add'], instructor['tests']['ru']['add']],
    state=TestStates.process
)
async def requesting_subject_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))
    subjects = await subject_controller.get_all(dict(status=StatusChoices.ACTIVE))
    sections = await section_controller.get_all(dict(user_id=user.id, status=StatusChoices.ACTIVE))

    if len(sections) <= 0:
        error_message = translator(
            "Hali bo'lim qo'shmaganingiz uchun test qo'sha olmaysiz",
            "Вы не можете добавить тест, потому что вы еще не добавили раздел",
            user.lang
        )
        await message.answer(error_message)
        return

    if len(subjects) <= 0:
        error_message = translator(
            "Hali fanlar qo'shilmagani uchun test qo'sha olmaysiz",
            "Вы не можете добавить тест, потому что еще не добавлено ни одного предмета",
            user.lang
        )
        await message.answer(error_message)
        return

    await TestStates.subject.set()

    message_text = translator(
        "Qaysi fan uchun test qo'shmoqchisiz", "Для какого предмета вы хотите добавить тест", user.lang
    )

    await message.answer(text=message_text, reply_markup=subjects_sections_keyboard(subjects, user.lang, 3))


@dp.message_handler(IsInstructor(), state=TestStates.subject)
async def requesting_section_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)

        await message.answer(error_message)
        await instructor_tests_handler(message, state)
        return

    query = translator(dict(name_uz=message.text), dict(name_ru=message.text), user.lang)

    subject_checking = await subject_controller.get_one(query)

    if not subject_checking:
        error_message = translator(
            "Berilgan fanlardan birini tanlang", "Выберите один из предложенных предметов", user.lang
        )
        await message.answer(error_message)
        return

    async with state.proxy() as data:
        data['test_subject'] = subject_checking.id

    await TestStates.section.set()

    sections = await section_controller.get_all(
        dict(user_id=user.id, subject_id=subject_checking.id, status=StatusChoices.ACTIVE)
    )

    if not sections:
        error_message = translator(
            "Hali bu fan uchun bo'lim qo'shmagansiz", "Вы еще не добавили раздел по этой теме", user.lang
        )
        await TestStates.process.set()
        await message.answer(error_message, reply_markup=instructor_keyboard(TEST, user.lang))
        return

    message_text = translator(
        "Qaysi bo'lim uchun test qo'shmoqchisiz", "Для какого секции вы хотите добавить тест", user.lang
    )

    await message.answer(message_text, reply_markup=subjects_sections_keyboard(sections, user.lang))


@dp.message_handler(IsInstructor(), state=TestStates.section)
async def requesting_image_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)

        await message.answer(error_message)
        await instructor_tests_handler(message, state)
        return

    query = translator(dict(name_uz=message.text), dict(name_ru=message.text), user.lang)

    section_checking = await section_controller.get_one(query)

    if not section_checking:
        error_message = translator(
            "Berilgan fanlardan birini tanlang", "Выберите один из предложенных предметов", user.lang
        )
        await message.answer(error_message)
        return

    async with state.proxy() as data:
        data['test_section'] = section_checking.id

    await TestStates.image.set()

    message_text = translator(
        "Test uchun rasm yuboring. Test uchun rasm kerak bo'lmasa keyingi tugmasini bosing",
        "Присылайте фото на пробу. Если вам не нужно изображение для теста, нажмите кнопку «Далее»",
        user.lang
    )

    await message.answer(message_text, reply_markup=next_keyboard(user.lang))


# @dp.message_handler(IsInstructor(), content_types=[ContentTypes.PHOTO, ContentTypes.TEXT], state=TestStates.image)
@dp.message_handler(IsInstructor(), content_types=ContentTypes.ANY, state=TestStates.image)
async def requesting_question_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    message_text = translator("Test savolini yuboring", "Отправьте вопрос теста", user.lang)

    path = join(dirname(abspath(__file__)), '..', '..', '..', 'test_app', 'static', 'media', 'test_photos')

    if not await to_thread(exists, path):
        await to_thread(mkdir, path)

    if message.text:
        if is_num(message.text):
            error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
            await message.answer(error_message)
            return

        if message.text in [option['back']['uz'], option['back']['ru']]:
            error_message = translator("Bekor qilindi", "Отменено", user.lang)

            await message.answer(error_message)
            await instructor_tests_handler(message, state)
            return

        if message.text in [option['next']['uz'], option['next']['ru']]:
            await TestStates.question.set()

            async with state.proxy() as data:
                data['test_image'] = ''

            await message.answer(message_text, reply_markup=back_keyboard(user.lang))
            return

    await TestStates.question.set()

    async with state.proxy() as data:
        data['test_image'] = message.photo[0].file_id

    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsInstructor(), state=TestStates.question)
async def requesting_variants_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)

        await message.answer(error_message)
        await instructor_tests_handler(message, state)
        return

    await TestStates.variants.set()

    async with state.proxy() as data:
        data['test_question'] = message.text

    message_text = translator(
        (
            "Variantlarni ketma ket qator tashlab yozing. Masalan:\n"
            "\nAlisher Navoiy\n"
            "Amir Temur\n"
            "\nVariantlar 1 tadan ko'p bo'lishi kerak"
        ),
        (
            "Введите параметры в последовательных строках. Например:\n"
            "\nАлишер Навоий\n"
            "Амир Темур\n"
            "\nВариантов должно быть больше 1"
        ),
        user.lang
    )

    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsInstructor(), state=TestStates.variants)
async def requesting_correct_answer_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)

        await message.answer(error_message)
        await instructor_tests_handler(message, state)
        return

    await TestStates.correct_answer.set()

    async with state.proxy() as data:
        data['test_variants'] = message.text

    message_text = translator("Testning to'g'ri javobini yuboring", "Отправьте правильный ответ на тест", user.lang)

    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsInstructor(), state=TestStates.correct_answer)
async def checking_creation_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)

        await message.answer(error_message)
        await instructor_tests_handler(message, state)
        return

    await TestStates.checking.set()

    async with state.proxy() as data:
        data['test_correct_answer'] = message.text

    data = await state.get_data()

    subject = await subject_controller.get_one(dict(id=data['test_subject']))
    section = await section_controller.get_one(dict(id=data['test_section']))

    dope = dict(
        owner=user.name,
        subject=translator(subject.name_uz, subject.name_ru, user.lang),
        section=translator(section.name_uz, section.name_ru, user.lang),
        question=data['test_question'],
        variants=data['test_variants'].split('\n'),
        correct_answer=message.text
    )

    await message.answer(test_format(dope, user.lang, True), reply_markup=confirmation_keyboard(user.lang))


@dp.message_handler(IsInstructor(), state=TestStates.checking)
async def test_creation_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text not in [
        option['confirmation']['uz'], option['confirmation']['uz'],
        option['confirmation']['ru'], option['confirmation']['ru']
    ]:
        error_message = translator(
            "Sizga taqdim etilgan ugmalardan birini bosing", "Нажмите на один из предложенных вам вариантов", user.lang
        )
        await message.answer(error_message)
        return

    if message.text in [option['confirmation_advertising']['uz']['no'], option['confirmation_advertising']['ru']['no']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)

        await message.answer(error_message, reply_markup=instructor_keyboard(TEST, user.lang))
        return

    data = await state.get_data()

    translator_language = translator("ru", 'uz', user.lang)

    translated_question = GoogleTranslator(target=translator_language).translate(data['test_question']).capitalize()
    translated_correct_answer = GoogleTranslator(target=translator_language).translate(
        data['test_correct_answer']
    ).capitalize()

    variants = []

    for variant in data['test_variants'].split('\n'):
        translated_variant = GoogleTranslator(target=translator_language).translate(variant).capitalize()
        variants.append(translated_variant)

    question_uz, question_ru, correct_answer_uz, correct_answer_ru, variants_uz, variants_ru = '', '', '', '', [], []

    if translator_language == 'uz':
        question_uz = translated_question
        question_ru = data['test_question']
        correct_answer_uz = translated_correct_answer
        correct_answer_ru = data['test_correct_answer']
        variants_uz = variants
        variants_ru = data['test_variants'].split('\n')
    elif translator_language == 'ru':
        question_uz = data['test_question']
        question_ru = correct_answer_ru
        correct_answer_uz = data['test_correct_answer']
        correct_answer_ru = translated_correct_answer
        variants_uz = data['test_variants'].split('\n')
        variants_ru = variants

    if data['test_image'] != '':
        path = join(dirname(abspath(__file__)), '..', '..', '..', 'test_app', 'static', 'media', 'test_photos',
                    f'{question_uz}.jpg')

        photo_file = await dp.bot.download_file_by_id(data['test_image'])

        async with aiofiles.open(path, "wb") as f:
            await f.write(photo_file.getvalue())

    await test_controller.make(
        dict(
            user_id=user.id,
            subject_id=data['test_subject'],
            section_id=data['test_section'],
            image=data['test_image'],
            question_uz=question_uz,
            question_ru=question_ru,
            variants_uz=variants_uz,
            variants_ru=variants_ru,
            correct_answer_uz=correct_answer_uz,
            correct_answer_ru=correct_answer_ru
        )
    )

    async with state.proxy() as data:
        del data['test_subject']
        del data['test_section']
        del data['test_image']
        del data['test_question']
        del data['test_variants']
        del data['test_correct_answer']

    await TestStates.process.set()

    message_text = translator("Yangi test qo'shildi", "Новый предмет тест", user.lang)

    await message.answer(message_text, reply_markup=instructor_keyboard(TEST, user.lang))
