from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from bot.loader import dp
from bot.controllers import user_controller
from bot.helpers.formats import user_format
from bot.helpers.utils import is_num, translator
from bot.keyboards.keyboard_buttons import admin, option, all
from bot.keyboards.keyboards import (
    settings_keyboard,
    language_keyboard,
    back_keyboard
)
from bot.states.settings import SettingsStates
from bot.states.user import UserStates


@dp.message_handler(text=[admin['pages']['uz']['settings'], admin['pages']['ru']['settings']], state=UserStates.process)
async def user_settings_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    await SettingsStates.process.set()

    await message.answer(
        text=user_format(user, user.lang),
        reply_markup=settings_keyboard(user.lang)
    )


@dp.message_handler(
    text=[all['settings']['uz']['name'], all['settings']['ru']['name']], state=SettingsStates.process
)
async def requesting_user_name_for_update_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    message_text = translator(
        "O'zgartirmoqchi bo'lgan ismingizni kiriting", "Введите имя, которое хотите изменить", user.lang
    )

    await SettingsStates.name.set()
    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(state=SettingsStates.name)
async def updating_user_name_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)
        await message.answer(error_message)
        await user_settings_handler(message, state)
        return

    if is_num(message.text):
        error_message = translator("Raqam jo'natmang!", "Не присылайте номер!", user.lang)
        await message.answer(error_message)
        return

    await user.update(name=message.text).apply()

    await SettingsStates.process.set()

    await message.answer(
        text=user_format(user, user.lang),
        reply_markup=settings_keyboard(user.lang)
    )

    message_text = translator("Ismingiz muvaffaqiyatli o'zgartirildi", "Ваше имя успешно изменено", user.lang)

    await message.answer(message_text)


@dp.message_handler(
    text=[all['settings']['uz']['number'], all['settings']['ru']['number']],
    state=SettingsStates.process
)
async def requesting_user_number_for_update_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    message_text = translator(
        "O'zgartirmoqchi bo'lgan raqamingizni kiriting",
        "Введите номер, которое хотите изменить",
        user.lang
    )

    await SettingsStates.number.set()
    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(state=SettingsStates.number)
async def updating_user_number_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)
        await message.answer(error_message)
        await user_settings_handler(message, state)
        return

    if not is_num(message.text):
        error_message = translator("Raqam jo'nating!", "Пришлите номер!", user.lang)
        await message.answer(error_message)
        return

    await user.update(number=message.text).apply()

    await SettingsStates.process.set()

    await message.answer(
        text=user_format(user, user.lang),
        reply_markup=settings_keyboard(user.lang)
    )

    message_text = translator("Raqamingiz muvaffaqiyatli o'zgartirildi", "Ваше номер успешно изменено", user.lang)

    await message.answer(message_text)


@dp.message_handler(
    text=[all['settings']['uz']['lang'], all['settings']['ru']['lang']], state=SettingsStates.process
)
async def requesting_user_lang_for_update_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    message_text = translator("Qaysi tilni tanlaysiz", "Какой язык вы выбираете", user.lang)

    await SettingsStates.lang.set()
    await message.answer(message_text, reply_markup=language_keyboard(is_editing=True, language=user.lang))


@dp.message_handler(state=SettingsStates.lang)
async def updating_user_lang_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text in [option['back']['uz'], option['back']['ru']]:
        error_message = translator("Bekor qilindi", "Отменено", user.lang)
        await message.answer(error_message)
        await user_settings_handler(message, state)
        return

    if is_num(message.text):
        error_message = translator("Raqam jo'nating!", "Пришлите номер!", user.lang)
        await message.answer(error_message)
        return

    if message.text not in [option['language']['uz'], option['language']['ru']]:
        error_message = translator(
            "O'zingizga mos keladigan tugmani bosib tilni tanlang",
            "Выберите язык, который вам подходит, нажав на кнопку",
             user.lang
        )
        await message.answer(error_message)
        return

    await user.update(lang=message.text).apply()

    await SettingsStates.process.set()

    await message.answer(
        text=user_format(user, user.lang),
        reply_markup=settings_keyboard(user.lang)
    )

    message_text = translator(
        "Platformadagi tilingiz muvaffaqiyatli o'zgartirildi", "Язык вашей платформы успешно изменен", user.lang
    )

    await message.answer(message_text)
