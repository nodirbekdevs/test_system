from aiogram.types import Message, CallbackQuery, ContentTypes
from aiogram.dispatcher import FSMContext

from os import mkdir, remove
from os.path import join, exists, dirname, abspath

import aiofiles
from asyncio import to_thread

from bot.loader import dp
from bot.controllers import user_controller, advertising_controller
from bot.models.advertising import StatusChoices
from bot.filters.is_admin import IsAdmin
from bot.helpers.formats import advertising_format, advertising_number_format
from bot.helpers.utils import Pagination, translator
from bot.keyboards.keyboard_buttons import admin, option
from bot.keyboards.keyboards import (
    admin_advertisements_keyboard,
    one_advertising_keyboard,
    confirmation_advertising_keyboard,
    back_keyboard,
)
from bot.states.advertising import AdvertisingStates
from bot.states.user import UserStates


@dp.message_handler(
    IsAdmin(),
    text=[admin['pages']['uz']['advertisements'], admin['pages']['ru']['advertisements']],
    state=UserStates.process
)
async def admin_advertisements_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.chat.id))

    await AdvertisingStates.process.set()

    message_text = translator("Reklamalar bo'limi", "Рекламный отдел", user.lang)

    await message.answer(message_text, reply_markup=admin_advertisements_keyboard(user.lang))


@dp.message_handler(
    IsAdmin(),
    text=[admin['advertisements']['uz']['number'], admin['advertisements']['ru']['number']],
    state=AdvertisingStates.process
)
async def number_of_advertisements_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    number = await advertising_controller.count(dict())
    active = await advertising_controller.count(dict(status=StatusChoices.ACTIVE))
    inactive = await advertising_controller.count(dict(status=StatusChoices.IN_ACTIVE))

    await message.answer(
        advertising_number_format(dict(number=number, active=active, inactive=inactive), user.lang)
    )


@dp.message_handler(
    IsAdmin(),
    text=[admin['advertisements']['uz']['all'], admin['advertisements']['ru']['all']],
    state=AdvertisingStates.process
)
async def all_advertisements_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    await AdvertisingStates.all_advertisements.set()

    paginated = await Pagination('ADVERTISING').paginate(1, 6, dict(status=StatusChoices.ACTIVE), user.lang)

    if not paginated['status']:
        await AdvertisingStates.process.set()

    await message.answer(paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(
    IsAdmin(),
    lambda query: query.data.startswith("left#advertising#") or query.data.startswith("right#advertising#"),
    state=AdvertisingStates.all_advertisements
)
async def paginate_advertisements_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))
    page = int(query.data.split('#')[2])
    paginated = await Pagination('ADVERTISING').paginate(page, 6, dict(status=StatusChoices.ACTIVE), user.lang)
    await query.message.edit_text(paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == 'delete', state=AdvertisingStates.all_advertisements)
async def back_from_advertisements_pagination_handler(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await admin_advertisements_handler(query.message, state)


@dp.callback_query_handler(
    IsAdmin(), lambda query: query.data.startswith("sadver-"), state=AdvertisingStates.all_advertisements
)
async def one_advertising_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    id = int(query.data.split("-")[1])

    advertising = await advertising_controller.get_one(dict(id=id))

    dope = dict(title=advertising.title, description=advertising.description)

    await AdvertisingStates.one_advertising.set()

    await query.message.delete()

    async with aiofiles.open(advertising.file, 'rb') as file:
        await query.message.answer_photo(
            file,
            caption=advertising_format(dope, user.lang),
            reply_markup=one_advertising_keyboard(id, user.lang)
        )


@dp.callback_query_handler(IsAdmin(), lambda query: query.data == 'back', state=AdvertisingStates.one_advertising)
async def back_from_one_advertising_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    await AdvertisingStates.all_advertisements.set()
    paginated = await Pagination('ADVERTISING').paginate(1, 6, dict(status=StatusChoices.ACTIVE), user.lang)

    await query.message.delete()

    await AdvertisingStates.all_advertisements.set()

    if not paginated['status']:
        AdvertisingStates.process.set()

    await query.message.answer(paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(
    IsAdmin(), lambda query: query.data.startswith("send_ad."), state=AdvertisingStates.one_advertising
)
async def send_advertising_to_all_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    id = int(query.data.split('.')[1])

    advertising = await advertising_controller.get_one(dict(id=id))

    dope = dict(title=advertising.title, description=advertising.description)

    users = await user_controller.get_all(dict(status=StatusChoices.ACTIVE))

    for user in users:
        async with aiofiles.open(advertising.file, 'rb') as image:
            await dp.bot.send_photo(user.telegram_id, image, advertising_format(dope, user.lang))

    await AdvertisingStates.all_advertisements.set()

    paginated = await Pagination('ADVERTISING').paginate(1, 6, dict(status=StatusChoices.ACTIVE), user.lang)

    await query.message.delete()

    if not paginated['status']:
        await AdvertisingStates.process.set()

    await query.message.answer(paginated['message'], reply_markup=paginated['keyboard'])

    message_text = translator("Reklama barchaga yuborildi", "Объявление отправлено всем", user.lang)

    await query.message.answer(message_text)


@dp.callback_query_handler(
    IsAdmin(), lambda query: query.data.startswith("delete_ad."), state=AdvertisingStates.one_advertising
)
async def delete_advertising_handler(query: CallbackQuery, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=query.from_user.id))

    id = int(query.data.split('.')[1])

    advertising = await advertising_controller.get_one(dict(id=id))

    deleting_path = join(
        dirname(
            abspath(__file__)
        ), '..', '..', '..', 'test_app', 'static', 'media', 'advertising_photos', f'{advertising.title}.jpg'
    )

    await to_thread(remove, deleting_path)

    await advertising_controller.delete(dict(id=id))

    await AdvertisingStates.all_advertisements.set()

    paginated = await Pagination('ADVERTISING').paginate(1, 6, dict(status=StatusChoices.ACTIVE), user.lang)

    await query.message.delete()

    if not paginated['status']:
        await AdvertisingStates.process.set()

    message_text = translator("Reklama o'chirildi", "Объявление удалено", user.lang)

    await query.message.answer(message_text)

    await query.message.answer(paginated['message'], reply_markup=paginated['keyboard'])


@dp.message_handler(
    IsAdmin(),
    text=[admin['advertisements']['uz']['add'], admin['advertisements']['uz']['add']],
    state=AdvertisingStates.process
)
async def requesting_advertising_image_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))
    await AdvertisingStates.image.set()

    message_1 = translator("Reklama joylashga hush kelibsiz", "Вы можете разместить объявление", user.lang)
    message_2 = translator("Reklamani rasmini jo'nating", "Отправьте фото объявления", user.lang)

    await message.answer(message_1)
    await message.answer(message_2, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsAdmin(), content_types=ContentTypes.ANY, state=AdvertisingStates.image)
async def requesting_advertising_title_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text in [option['back']['uz'], option['back']['ru']]:
        await AdvertisingStates.process.set()
        error_message = translator("Bekor qilindi", "Отменено", user.lang)
        await message.answer(error_message, reply_markup=admin_advertisements_keyboard(user.lang))
        return

    path = join(dirname(abspath(__file__)), '..', '..', '..', 'test_app', 'static', 'media', 'advertising_photos')

    if not await to_thread(exists, path):
        await to_thread(mkdir, path)

    await AdvertisingStates.title.set()

    async with state.proxy() as data:
        data['advertising_image'] = message.photo[0].file_id

    message_text = translator("Reklamaning sarlavhasini kiriting", "Введите название объявления", user.lang)

    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsAdmin(), state=AdvertisingStates.title)
async def requesting_advertising_description_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text in [option['back']['uz'], option['back']['ru']]:
        await AdvertisingStates.process.set()
        error_message = translator("Bekor qilindi", "Отменено", user.lang)
        await message.answer(error_message, reply_markup=admin_advertisements_keyboard(user.lang))
        return

    async with state.proxy() as data:
        data['advertising_title'] = message.text

    message_text = translator("Reklamaning tavsifini kiriting", "Введите описание объявления", user.lang)

    await AdvertisingStates.description.set()
    await message.answer(message_text, reply_markup=back_keyboard(user.lang))


@dp.message_handler(IsAdmin(), state=AdvertisingStates.description)
async def check_advertising_creation_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text in [option['back']['uz'], option['back']['ru']]:
        await AdvertisingStates.process.set()
        error_message = translator("Bekor qilindi", "Отменено", user.lang)
        await message.answer(error_message, reply_markup=admin_advertisements_keyboard(user.lang))
        return

    data = await state.get_data()

    image, title, description = data.get("advertising_image"), data.get("advertising_title"), message.text

    async with state.proxy() as data:
        data['advertising_description'] = message.text

    await AdvertisingStates.checking.set()

    await message.answer_photo(
        image,
        caption=advertising_format(data=dict(title=title, description=description), is_ending=True, language=user.lang),
        reply_markup=confirmation_advertising_keyboard(user.lang)
    )


@dp.message_handler(IsAdmin(), state=AdvertisingStates.checking)
async def advertising_creation_handler(message: Message, state: FSMContext):
    user = await user_controller.get_one(dict(telegram_id=message.from_user.id))

    if message.text not in [
        option['confirmation_advertising']['uz']['no'], option['confirmation_advertising']['uz']['yes'],
        option['confirmation_advertising']['ru']['no'], option['confirmation_advertising']['ru']['yes']
    ]:
        error_message = translator(
            "Sizga taqdim etilgan ugmalardan birini bosing", "Нажмите на один из предложенных вам вариантов", user.lang
        )

        await message.answer(
            text=error_message,
            reply_markup=admin_advertisements_keyboard(user.lang)
        )
        return

    if message.text in [option['confirmation_advertising']['uz']['no'], option['confirmation_advertising']['ru']['no']]:
        await AdvertisingStates.process.set()

        error_message = translator("Bekor qilindi", "Отменено", user.lang)
        await message.answer(error_message, reply_markup=admin_advertisements_keyboard(user.lang))
        return

    data, admin = await state.get_data(), await user_controller.get_one(dict(telegram_id=message.from_user.id))

    image, title, description = data.get("advertising_image"), data.get("advertising_title"), data.get(
        "advertising_description")

    path = join(dirname(abspath(__file__)), '..', '..', '..', 'test_app', 'static', 'media', 'advertising_photos', f'{title}.jpg')

    audio_file = await dp.bot.download_file_by_id(image)

    await AdvertisingStates.process.set()

    async with aiofiles.open(path, "wb") as f:
        await f.write(audio_file.getvalue())

    await advertising_controller.make(
        dict(user_id=admin.id, image=image, file=path, title=title, description=description)
    )

    await message.answer_photo(
        photo=image,
        caption=advertising_format(dict(title=title, description=description), user.lang),
        reply_markup=admin_advertisements_keyboard(user.lang)
    )
