import aiofiles
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from random import sample

from bot.loader import dp
from bot.controllers import user_controller, section_controller, test_controller, subject_controller
from bot.models.user import User
from bot.models.test import StatusChoices
from bot.keyboards.keyboards import (
    subjects_sections_keyboard, student_pages_keyboard, all_users_keyboard, start_test_keyboard, test_solution_keyboard
)
from bot.filters.is_student import IsStudent
from bot.keyboards.keyboard_buttons import student, option
from bot.helpers.utils import is_num, translator
from bot.helpers.formats import checking_solved_tests_format, test_solution_format, back_format
from bot.states.test import TestStates
from bot.states.user import UserStates


@dp.message_handler(
    IsStudent(),
    text=[student['pages']['uz']['tests'], student['pages']['ru']['tests']],
    state=UserStates.process
)
async def student_tests_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    subjects = await subject_controller.get_all(dict(status=StatusChoices.ACTIVE))

    message_text = translator(
        "Nima fandan test yechmoqchisiz", "По какому предмету вы хотите пройти тест?", user.lang
    )

    await TestStates.choose_subject.set()

    await message.answer(message_text, reply_markup=subjects_sections_keyboard(subjects, user.lang))


@dp.message_handler(
    IsStudent(),
    state=TestStates.choose_subject
)
async def get_subject_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = back_format(user.lang)
        await UserStates.process.set()
        await message.answer(error_message, reply_markup=student_pages_keyboard(user.lang))
        return

    subject_query = translator(dict(name_uz=message.text), dict(name_ru=message.text), user.lang)

    subject = await subject_controller.get_one(subject_query)

    if not subject:
        error_message = translator(
            "Berilgan fanlardan birini tanlang", "Выберите один из предложенных предметов", user.lang
        )

        await message.answer(error_message)
        return

    instructors = await user_controller.get_all(dict(type=User.TypeChoices.INSTRUCTOR, subject_id=subject.id))

    message_text = translator(
        "Qaysi instructorni testlarini yechmoqchisiz", "Какой инструктор вы хотите решить тесты", user.lang
    )

    await TestStates.choose_instructor.set()

    await message.answer(message_text, reply_markup=all_users_keyboard(instructors, user.lang, 3))


@dp.message_handler(
    IsStudent(),
    state=TestStates.choose_instructor
)
async def get_instructor_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = back_format(user.lang)
        await UserStates.process.set()
        await message.answer(error_message, reply_markup=student_pages_keyboard(user.lang))
        return

    instructor = await user_controller.get_one(dict(name=message.text, status=StatusChoices.ACTIVE))

    print(instructor)

    if not instructor:
        error_message = translator(
            "Berilgan instruktorlardan birini tanlang", "Выберите один из предложенных инструкторов", user.lang
        )

        await message.answer(error_message)
        return

    sections = await section_controller.get_all(dict(user_id=instructor.id, status=StatusChoices.ACTIVE))

    test_exist_sections = []

    for section in sections:
        tests = await test_controller.get_all(
            dict(subject_id=section.subject_id, section_id=section.id, status=StatusChoices.ACTIVE)
        )

        if len(tests) >= 4:
            test_exist_sections.append(section)

    message_text = translator(
        "Qaysi bo'limdagi testlarini yechmoqchisiz", "В каком разделе вы хотите решить тесты", user.lang
    )

    await TestStates.choose_section.set()

    await message.answer(message_text, reply_markup=subjects_sections_keyboard(test_exist_sections, user.lang, 3))


@dp.message_handler(
    IsStudent(),
    state=TestStates.choose_section
)
async def request_start_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = back_format(user.lang)
        await UserStates.process.set()
        await message.answer(error_message, reply_markup=student_pages_keyboard(user.lang))
        return

    section_query = translator(dict(name_uz=message.text), dict(name_ru=message.text), user.lang)

    section = await section_controller.get_one(section_query)

    if not section:
        error_message = translator(
            "Berilgan bo'limlardan birini tanlang", "Выберите один из предложенных секции", user.lang
        )

        await message.answer(error_message)
        return

    tests = await test_controller.get_all(
        dict(subject_id=section.subject_id, section_id=section.id, status=StatusChoices.ACTIVE)
    )

    random_tests = sample(tests, 4)

    dictionary_random_tests = []

    for random_test in random_tests:
        test = random_test.__dict__
        dictionary_random_tests.append(test['__values__'])

    async with state.proxy() as data:
        data['tests'] = dictionary_random_tests

    message_text = translator("Jarayon boshlanmoqda", "Процесс начинается", user.lang)

    await TestStates.start_test.set()

    await message.answer(message_text, reply_markup=start_test_keyboard(user.lang))


@dp.callback_query_handler(IsStudent(), lambda query: query.data in ['start_test'], state=TestStates.start_test)
async def start_test_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    data = await state.get_data()

    test = data['tests'][0]

    async with state.proxy() as data:
        data['solving_test_id'] = test['id']

    message_text, keyboard = test_solution_format(test, user.lang), test_solution_keyboard(test, user.lang)

    await TestStates.solving_test.set()

    await test_controller.update(dict(id=test['id']), dict(is_testing=True))

    if test['image']:
        async with aiofiles.open(test['image'], 'rb') as file:
            await query.message.answer_photo(file, caption=message_text, reply_markup=keyboard)
            return

    await query.message.delete()
    await query.message.answer(text=message_text, reply_markup=keyboard)


@dp.callback_query_handler(IsStudent(), lambda query: query.data in ['delete'], state=TestStates.solving_test)
async def back_from_solving_test_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    data = await state.get_data()

    test = data['solving_test_id']

    await test_controller.update(dict(id=test), dict(is_testing=False))

    async with state.proxy() as data:
        del data['tests']
        del data['solving_test_id']

        if data['solved_tests']:
            del data['solved_tests']

    message_text = translator('Bosh sahifa', 'Домашняя страница', user.lang)

    await UserStates.process.set()

    await query.message.delete()

    await query.message.answer(message_text, reply_markup=student_pages_keyboard(user.lang))


@dp.callback_query_handler(IsStudent(), lambda query: query.data in ['prev_test'], state=TestStates.solving_test)
async def prev_test_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    data = await state.get_data()

    tests, solving_test, solved_tests = data['tests'], data['solving_test_id'], data.get('solved_tests')

    current_test_index = 0

    for test in tests:
        if test['id'] == solving_test:
            current_test_index = tests.index(test)

    if current_test_index == 0:
        warning_message = translator(
            "Bundan oldin test mavjud emas bu birinchi test", "Нет теста, прежде чем это первый тест", user.lang
        )

        await query.answer(text=warning_message, show_alert=True)
        return

    prev_test = tests[current_test_index-1]

    solved_test_answer = False

    if solved_tests:
        for solved_test in solved_tests:
            if solved_test['id'] == prev_test['id']:
                solved_test_answer = solved_test['answer']

    await test_controller.update(dict(id=solving_test), dict(is_testing=False))
    await test_controller.update(dict(id=prev_test['id']), dict(is_testing=True))

    async with state.proxy() as data:
        data['solving_test_id'] = prev_test['id']

    message_text, keyboard = test_solution_format(prev_test, user.lang), test_solution_keyboard(prev_test, user.lang, solved_test_answer)

    if prev_test['image'] != '':
        await query.message.delete()
        async with aiofiles.open(prev_test['image'], 'rb') as file:
            await query.message.answer_photo(file, caption=message_text, reply_markup=keyboard)
            return

    await query.message.edit_text(text=message_text, reply_markup=keyboard)


@dp.callback_query_handler(IsStudent(), lambda query: query.data in ['next_test'], state=TestStates.solving_test)
async def next_test_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    data = await state.get_data()

    tests, solving_test, solved_tests = data['tests'], data['solving_test_id'], data.get('solved_tests')

    current_test_index = 0

    for test in tests:
        if test['id'] == solving_test:
            current_test_index = tests.index(test)

    if current_test_index == 3:
        warning_message = translator(
            "Bundan keyin test mavjud emas bu ohirgi test", "После этого теста нет, это последний тест", user.lang
        )

        await query.answer(text=warning_message, show_alert=True)
        return

    next_test = tests[current_test_index+1]

    solved_test_answer = False

    if solved_tests:
        for solved_test in solved_tests:
            if solved_test['id'] == next_test['id']:
                solved_test_answer = solved_test['answer']

    await test_controller.update(dict(id=solving_test), dict(is_testing=False))
    await test_controller.update(dict(id=next_test['id']), dict(is_testing=True))

    async with state.proxy() as data:
        data['solving_test_id'] = next_test['id']

    message_text, keyboard = test_solution_format(next_test, user.lang), test_solution_keyboard(next_test, user.lang, solved_test_answer)

    if next_test['image'] != '':
        await query.message.delete()
        async with aiofiles.open(next_test['image'], 'rb') as file:
            await query.message.answer_photo(file, caption=message_text, reply_markup=keyboard)
            return

    await query.message.edit_text(text=message_text, reply_markup=keyboard)


@dp.callback_query_handler(IsStudent(), lambda query: query.data.startswith('solving_'), state=TestStates.solving_test)
async def solve_test_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    state_data = await state.get_data()

    tests, solving_test_id, solved_tests = state_data['tests'], state_data['solving_test_id'], state_data.get('solved_tests')

    solving_test_answer = query.data.split('_')[1]

    found_match, current_test_index = False, 0

    if solved_tests is None:
        solved_tests = []

    solving_test_dict = dict(id=solving_test_id, answer=solving_test_answer)

    if solved_tests:
        for solved_test in solved_tests:
            if solved_test['id'] == solving_test_id:
                solved_test['answer'] = solving_test_answer
                found_match = True

    if not found_match:
        solved_tests.append(solving_test_dict)

    for test in tests:
        if test['id'] == solving_test_id:
            current_test_index = tests.index(test)

    async with state.proxy() as data:
        data['solved_tests'] = solved_tests

    print(solved_tests)

    if current_test_index != 3:
        next_test = tests[current_test_index + 1]

        answer = False

        if current_test_index + 1 < len(solved_tests):
            answer = solved_tests[current_test_index + 1]['answer'] if solved_tests[current_test_index + 1] else False

        print(answer)

        message_text = test_solution_format(next_test, user.lang)
        keyboard = test_solution_keyboard(next_test, user.lang, answer)

        async with state.proxy() as data:
            data['solving_test_id'] = next_test['id']

        if next_test['image'] != '':
            await query.message.delete()
            async with aiofiles.open(next_test['image'], 'rb') as file:
                await query.message.answer_photo(file, caption=message_text, reply_markup=keyboard)
                return

        await query.message.edit_text(text=message_text, reply_markup=keyboard)
        return

    warning_message = translator("Testlar qolmadi", "Тесты закончились", user.lang)

    test = await test_controller.get_one(dict(id=solving_test_id))

    message_text = test_solution_format(test.__dict__['__values__'], user.lang)
    keyboard = test_solution_keyboard(test.__dict__['__values__'], user.lang, solving_test_answer)

    if test.image != '':
        await query.message.delete()
        async with aiofiles.open(test.image, 'rb') as file:
            await query.message.answer_photo(file, caption=message_text, reply_markup=keyboard)
            return

    await query.message.edit_text(text=message_text, reply_markup=keyboard)
    await query.answer(text=warning_message, show_alert=True)


@dp.callback_query_handler(IsStudent(), lambda query: query.data.startswith('finish_test'), state=TestStates.solving_test)
async def finish_test_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    state_data = await state.get_data()

    solved_tests = state_data['solved_tests']

    if len(solved_tests) == 0:
        message_text = translator('Bosh sahifa', 'Главная страница', user.lang)

        await UserStates.process.set()

        await query.message.delete()
        await query.message.answer(message_text, reply_markup=student_pages_keyboard(user.lang))

        async with state.proxy() as data:
            del data['tests']
            del data['solving_test_id']

            if data['solved_tests']:
                del data['solved_tests']

        return

    if len(solved_tests) != 4 and not state_data.get('ending_step'):
        await query.answer()

        message_text = translator(
            "Testlarni ohirigacha tugatmagansiz, Shunday holatda tugatishni hohlasangiz, yana 1 marotaba bosing.",
            "Вы не прошли тесты до конца, если хотите закончить в этом случае нажмите еще 1 раз.",
            user.lang
        )

        async with state.proxy() as data:
            data['ending_step'] = True

        await query.message.answer(message_text)
        return

    tests = state_data['tests']

    solved_tests_answers = {solved_test['id']: solved_test['answer'] for solved_test in solved_tests}

    total_score, number_solved_tests, checked_solved_tests = 0, 0, []

    for test in tests:
        correct_answer, test_id = translator(test['correct_answer_uz'], test['correct_answer_ru'], user.lang), test['id']

        if test_id in solved_tests_answers:
            answer = solved_tests_answers[test_id]

            test['answer'] = answer
            checked_solved_tests.append(test)

            if correct_answer == answer:
                # total_score += test['score']
                number_solved_tests += 1

    percentage = (number_solved_tests / len(tests)) * 100

    message_text = checking_solved_tests_format(checked_solved_tests, user.lang, percentage)

    print(number_solved_tests)

    await UserStates.process.set()

    await query.message.delete()
    await query.message.answer(message_text, reply_markup=student_pages_keyboard(user.lang))

    async with state.proxy() as data:
        del data['tests']
        del data['solving_test_id']
        del data['solved_tests']
        if data.get('ending_step'):
            del data['ending_step']