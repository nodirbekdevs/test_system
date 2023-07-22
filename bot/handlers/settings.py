from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from bot.loader import dp
from bot.controllers import user_controller
from bot.models.user import User
from bot.helpers.formats import user_format
from bot.helpers.utils import is_num
from bot.keyboards.keyboard_buttons import admin, option
from bot.keyboards.keyboards import (
    admin_settings_keyboard,
    language_keyboard,
    back_keyboard
)
from bot.states.settings import SettingsStates
from bot.states.user import UserStates


@dp.message_handler(text=[admin['pages']['uz']['settings'], admin['pages']['ru']['settings']], state=UserStates.process)
async def user_settings_handler(message: Message, state: FSMContext):
    received_user = await User.get_user_by_telegram_id(telegram_id=message.from_user.id)

    await SettingsStates.process.set()

    await message.answer(
        text=user_format(received_user, received_user.lang),
        reply_markup=admin_settings_keyboard(received_user.lang)
    )


@dp.message_handler(
    text=[admin['settings']['uz']['name'], admin['settings']['ru']['name']], state=SettingsStates.process
)
async def requesting_user_name_for_update_handler(message: Message, state: FSMContext):
    received_user = await User.get_user_by_telegram_id(telegram_id=message.from_user.id)

    message_text = "O'zgartirmoqchi bo'lgan ismingizni kiriting" \
        if received_user.lang == option['language']['uz'] else \
        "Введите имя, которое хотите изменить"

    await SettingsStates.name.set()
    await message.answer(message_text, reply_markup=back_keyboard(received_user.lang))


@dp.message_handler(state=SettingsStates.name)
async def updating_user_name_handler(message: Message, state: FSMContext):
    received_user = await User.get_user_by_telegram_id(telegram_id=message.from_user.id)

    if message.text in [option['back']['uz'], option['back']['ru']]:
        await user_settings_handler(message, state)
        return

    if is_num(message.text):
        error_message = "Raqam jo'nating!" if received_user.lang == option['language']['uz'] else "Пришлите номер!"
        await message.answer(error_message)
        return

    await received_user.update(name=message.text).apply()

    await SettingsStates.process.set()

    await message.answer(
        text=user_format(received_user, received_user.lang),
        reply_markup=admin_settings_keyboard(received_user.lang)
    )

    message_text = "Ismingiz muvaffaqiyatli o'zgartirildi" \
        if received_user.lang == option['language']['uz'] else \
        "Ваше имя успешно изменено"

    await message.answer(message_text)


@dp.message_handler(
    text=[admin['settings']['uz']['number'], admin['settings']['ru']['number']],
    state=SettingsStates.process
)
async def requesting_user_number_for_update_handler(message: Message, state: FSMContext):
    received_user = await User.get_user_by_telegram_id(telegram_id=message.from_user.id)

    message_text = "O'zgartirmoqchi bo'lgan raqamingizni kiriting" \
        if received_user.lang == option['language']['uz'] else \
        "Введите номер, которое хотите изменить"

    await SettingsStates.number.set()
    await message.answer(message_text, reply_markup=back_keyboard(received_user.lang))


@dp.message_handler(state=SettingsStates.number)
async def updating_user_number_handler(message: Message, state: FSMContext):
    received_user = await User.get_user_by_telegram_id(telegram_id=message.from_user.id)

    if message.text in [option['back']['uz'], option['back']['ru']]:
        await user_settings_handler(message, state)
        return

    if not is_num(message.text):
        error_message = "Raqam jo'nating!" if received_user.lang == option['language']['uz'] else "Пришлите номер!"
        await message.answer(error_message)
        return

    await received_user.update(number=message.text).apply()

    received_user = await User.get_user_by_telegram_id(telegram_id=message.from_user.id)

    await SettingsStates.process.set()

    await message.answer(
        text=user_format(received_user, received_user.lang),
        reply_markup=admin_settings_keyboard(received_user.lang)
    )

    message_text = "Raqamingiz muvaffaqiyatli o'zgartirildi" \
        if received_user.lang == option['language']['uz'] else \
        "Ваше номер успешно изменено"

    await message.answer(message_text)


@dp.message_handler(
    text=[admin['settings']['uz']['lang'], admin['settings']['ru']['lang']], state=SettingsStates.process
)
async def requesting_user_lang_for_update_handler(message: Message, state: FSMContext):
    received_user = await User.get_user_by_telegram_id(telegram_id=message.from_user.id)

    message_text = "Qaysi tilni tanlaysiz" if received_user.lang == option['language'][
        'uz'] else "Какой язык вы выбираете"

    await SettingsStates.lang.set()
    await message.answer(message_text, reply_markup=language_keyboard(is_editing=True, language=received_user.lang))


@dp.message_handler(state=SettingsStates.lang)
async def updating_user_lang_handler(message: Message, state: FSMContext):
    received_user = await User.get_user_by_telegram_id(telegram_id=message.from_user.id)

    if message.text in [option['back']['uz'], option['back']['ru']]:
        await user_settings_handler(message, state)
        return

    if is_num(message.text):
        error_message = "Raqam jo'natmang!" if received_user.lang == option['language'][
            'uz'] else "Не присылайте номер!"
        await message.answer(error_message)
        return

    if message.text not in [option['language']['uz'], option['language']['ru']]:
        error_message = "O'zingizga mos keladigan tugmani bosib tilni tanlang" \
            if received_user.lang == option['language']['uz'] else \
            "Выберите язык, который вам подходит, нажав на кнопку"
        await message.answer(error_message)
        return

    await received_user.update(lang=message.text).apply()

    received_user = await User.get_user_by_telegram_id(telegram_id=message.from_user.id)

    await SettingsStates.process.set()

    await message.answer(
        text=user_format(received_user, received_user.lang),
        reply_markup=admin_settings_keyboard(received_user.lang)
    )

    message_text = "Platformadagi tilingiz muvaffaqiyatli o'zgartirildi" \
        if received_user.lang == option['language']['uz'] else \
        "Язык вашей платформы успешно изменен"

    await message.answer(message_text)
