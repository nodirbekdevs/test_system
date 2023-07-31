from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from deep_translator import GoogleTranslator

from bot.loader import dp
from bot.filters.is_admin import IsAdmin
from bot.controllers import user_controller, subject_controller
from bot.models.subject import StatusChoices
from bot.keyboards.keyboards import admin_keyboard, one_admin_keyboard, back_keyboard, confirmation_keyboard
from bot.keyboards.keyboard_buttons import admin, option
from bot.helpers.utils import Pagination, is_num, translator
from bot.helpers.formats import subject_format
from bot.helpers.config import SUBJECT
from bot.states.subject import SubjectStates
from bot.states.user import UserStates


@dp.message_handler(
    IsAdmin(), text=[admin['pages']['uz']['subjects'], admin['pages']['ru']['subjects']], state=UserStates.process
)
async def admin_subjects_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.chat.id))

    message_text = translator("Fanlar sahifasi", "Страница предметов", user.lang)

    await SubjectStates.process.set()

    await message.answer(message_text, reply_markup=admin_keyboard(SUBJECT, user.lang))


@dp.message_handler(
    IsAdmin(), text=[admin['subjects']['uz']['all'], admin['subjects']['ru']['all']], state=SubjectStates.process
)
async def all_subjects_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    paginated = await Pagination("SUBJECT").paginate(1, 6, dict(status=StatusChoices.ACTIVE), user.lang)

    if paginated['status']:
        await SubjectStates.all_subjects.set()

    await message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == "delete", state=SubjectStates.all_subjects)
async def back_from_all_subjects_handler(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await admin_subjects_handler(query.message, state)


@dp.callback_query_handler(
    IsAdmin(),
    lambda query: query.data.startswith("left#subjects#") or query.data.startswith("right#subjects#"),
    state=SubjectStates.all_subjects
)
async def pagination_subjects_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    page = int(query.data.split("#")[2])

    paginated = await Pagination("SUBJECT").paginate(page, 6, dict(status=StatusChoices.ACTIVE), user.lang)

    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data.startswith("ssubject-"), state=SubjectStates.all_subjects)
async def get_subject_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    id = int(query.data.split("-")[1])

    selected_subject = await subject_controller.get_one(dict(id=id))

    data = dict(
        name=selected_subject.name_uz if user.lang == option['language']['uz'] else selected_subject.name_ru,
        description=selected_subject.description_uz if user.lang == option['language']['uz'] else selected_subject.description_ru,
        status=selected_subject.status,
        created_at=selected_subject.created_at
    )

    await SubjectStates.one_subject.set()

    await query.message.edit_text(
        text=subject_format(data, user.lang),
        reply_markup=one_admin_keyboard(id, user.lang, SUBJECT)
    )


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == "back", state=SubjectStates.one_subject)
async def back_from_get_subject_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    paginated = await Pagination("SUBJECT").paginate(1, 6, dict(status=StatusChoices.ACTIVE), user.lang)

    if paginated['status']:
        await SubjectStates.all_subjects.set()
        await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])
    else:
        await SubjectStates.process.set()
        await query.message.delete()
        await query.message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data.startswith("delete.subject."), state=SubjectStates.one_subject)
async def delete_subject_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    id = int(query.data.split(".")[2])

    await subject_controller.delete(dict(id=id))

    paginated = await Pagination("SUBJECT").paginate(1, 6, dict(status=StatusChoices.ACTIVE), user.lang)

    if not paginated['status']:
        await SubjectStates.process.set()
        await query.message.delete()
        await query.message.answer(text=paginated['message'], reply_markup=paginated['keyboard'])
    elif paginated['status']:
        await SubjectStates.all_subjects.set()
        await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.message_handler(
    IsAdmin(), text=[admin['subjects']['uz']['add'], admin['subjects']['ru']['add']], state=SubjectStates.process
)
async def requesting_name_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    await SubjectStates.name.set()

    message_text = translator("Fanni nomini yuboring", "Отправьте название предмета", user.lang)

    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsAdmin(), state=SubjectStates.name)
async def requesting_description_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)
        await message.answer(error_message)
        await admin_subjects_handler(message, state)
        return

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    subject_query = translator(dict(name_uz=message.text), dict(name_ru=message.text), user.lang)
    subject = await subject_controller.get_one(subject_query)

    if subject:
        error_message = translator("Bu fan bazada mavjud!", "Этот предмет существует в базе!", user.lang)
        await SubjectStates.process.set()
        await message.answer(error_message, reply_markup=admin_keyboard(SUBJECT, user.lang))
        return

    async with state.proxy() as data:
        data['subject_name'] = message.text

    await SubjectStates.description.set()

    message_text = translator("Fanni tavsifini yuboring", "Отправьте описание предмета", user.lang)

    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsAdmin(), state=SubjectStates.description)
async def checking_creation_subject_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)
        await message.answer(error_message)
        await admin_subjects_handler(message, state)
        return

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)

        await message.answer(error_message)
        return

    state_data = await state.get_data()

    subject_data = dict(name=state_data['subject_name'], description=message.text)

    async with state.proxy() as data:
        data['subject_description'] = message.text

    await SubjectStates.checking.set()

    await message.answer(subject_format(subject_data, user.lang, True), reply_markup=confirmation_keyboard(user.lang))


@dp.message_handler(IsAdmin(), state=SubjectStates.checking)
async def subject_creation_handler(message: Message, state: FSMContext):
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
        await message.answer(error_message,)
        return

    if message.text in [option['confirmation_advertising']['uz']['no'], option['confirmation_advertising']['ru']['no']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)

        await message.answer(error_message, reply_markup=admin_keyboard(SUBJECT, user.lang))
        return

    data = await state.get_data()

    translator_language = translator("ru", 'uz', user.lang)

    translated_subject_name = GoogleTranslator(target=translator_language).translate(data['subject_name']).capitalize()
    translated_subject_description = GoogleTranslator(target=translator_language).translate(data['subject_description']).capitalize()

    name_uz, name_ru, description_uz, description_ru = '', '', '', ''

    if translator_language == 'uz':
        name_uz = translated_subject_name
        name_ru = data['subject_name']
        description_uz = translated_subject_description
        description_ru = data['subject_description']
    elif translator_language == 'ru':
        name_uz = data['subject_name']
        name_ru = translated_subject_name
        description_uz = data['subject_description']
        description_ru = translated_subject_description

    await subject_controller.make(
        dict(name_uz=name_uz, name_ru=name_ru, description_uz=description_uz, description_ru=description_ru)
    )

    await SubjectStates.process.set()

    message_text = translator("Yangi fan qo'shildi", "Новый предмет добавлено", user.lang)

    await message.answer(message_text, reply_markup=admin_keyboard(SUBJECT, user.lang))
