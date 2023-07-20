from aiogram import Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberStatus
from bot.controllers import (
    section_controller, subject_controller, test_controller, user_controller
)
from bot.models.user import User
from bot.keyboards.keyboard_buttons import option
from bot.keyboards.keyboards import (
    admin_advertisements_keyboard,
    admin_admins_keyboard,
admin_subjects_keyboard,
admin_students_keyboard,
    admin_feedback_keyboard,
    admin_instructors_keyboard,
    instructor_sections_keyboard,
    instructor_tests_keyboard,
instructor_feedback_keyboard
)


class Pagination:
    def __init__(self, data_type: str):
        self.data_type = data_type

    async def paginate(self, page: int, limit: int, query: dict, language: str, form: str = '') -> dict:
        text, clause, data, all_data, keyboard, arr, author, status = "", "", [], [], InlineKeyboardMarkup(), [], {}, True

        offset = limit * (page - 1)

        if self.data_type == 'SUBJECT':
            data = await subject_controller.get_pagination(query, offset, limit)
            all_data = await subject_controller.get_all(query)
            clause = 'subjects'
        if self.data_type == 'SECTION':
            data = await section_controller.get_pagination(query, offset, limit)
            all_data = await section_controller.get_all(query)
            clause = 'sections'
        elif self.data_type == 'TEST':
            data = await test_controller.get_pagination(query, offset, limit)
            all_data = await test_controller.get_all(query)
            clause = 'tests'
        elif self.data_type == 'USER':
            data = await user_controller.get_pagination(query, offset, limit)
            all_data = await user_controller.get_all(query)
            clause = 'users'

        if len(data) <= 0:
            if self.data_type == 'SUBJECT':
                text = "Hozircha fanlar qo'shilmagan" \
                    if language == option['language']['uz'] else \
                    "Ни одна предмет еще не добавлена"

                keyboard = admin_subjects_keyboard(language)
            elif self.data_type == 'SECTION':
                text = "Hozircha bu tip uchun ismlar qo'shilmagan" \
                    if language == option['language']['uz'] else \
                    "Имена для этого типа пока не добавлены"

                keyboard = instructor_sections_keyboard(language)
            elif self.data_type == 'TEST':
                text = "Hozircha bu tip uchun testlar qo'shilmagan" \
                    if language == option['language']['uz'] else \
                    "Тесты для этого типа пока не добавлены"

                keyboard = instructor_tests_keyboard(language)
            elif self.data_type == 'PLACE':
                text = "Hozircha bu tip uchun tabriklar qo'shilmagan" \
                    if language == option['language']['uz'] else \
                    "Поздравления для этого типа пока не добавлены"
            elif self.data_type == 'ADVERTISING':
                text = "Hozircha reklamalar qo'shilmagan" \
                    if language == option['language']['uz'] else \
                    "Объявления еще не добавлены"

                keyboard = admin_advertisements_keyboard(language)
            elif self.data_type == 'FEEDBACK':
                if query['status'] == 'active':
                    text = 'Hali izohlar mavjud emas' if language == option['language']['uz'] else 'Комментариев пока нет'
                elif query['status'] == 'seen':
                    text = 'Hali bajarilayotgan izohlar mavjud emas' \
                        if language == option['language']['uz'] else \
                        "Комментариев пока нет"

                keyboard = instructor_feedback_keyboard(language) if 'author' in query else admin_feedback_keyboard(language)
            elif self.data_type == 'USER':
                text = "Hozircha adminlar topilmadi" \
                    if language == option['language']['uz'] else \
                    "Админы пока не найдены"

                if query['type'] == User.TypeChoices.ADMIN:
                    text = "Hozircha adminlar topilmadi" \
                        if language == option['language']['uz'] else \
                        "Админы пока не найдены"

                    keyboard = admin_admins_keyboard(language)
                elif query['type'] == User.TypeChoices.INSTRUCTOR:
                    text = "Hozircha instruktorlar topilmadi" \
                        if language == option['language']['uz'] else \
                        "Инструкторы пока не найдены"

                    keyboard = admin_instructors_keyboard(language)
                elif query['type'] == User.TypeChoices.STUDENT:
                    text = "Hozircha studentlar topilmadi" \
                        if language == option['language']['uz'] else \
                        "Студенты пока не найдены"

                    keyboard = admin_students_keyboard(language)

            status = False

            return dict(message=text, keyboard=keyboard, status=status)

        text = f'<b>Hozirgi: {offset + 1}-{len(data) + offset}, Jami: {len(all_data)}</b>\n\n' \
            if language == option['language']['uz'] else \
            f'<b>Текущий: {offset + 1}-{len(data) + offset}, Общий: {len(all_data)}</b>\n\n'

        for i, info in enumerate(data, start=1):
            callback_data = ""

            if self.data_type == 'SUBJECT':
                callback_data = f"ssubject-{info.id}"
            if self.data_type == 'SECTION':
                callback_data = f"ssection-{info.id}"
            elif self.data_type == 'PLACE':
                callback_data = f"splace-{info.id}"
            elif self.data_type == 'TEST':
                callback_data = f"stest-{info.id}"
            elif self.data_type == 'USER':
                callback_data = f"suser-{info.id}"
            elif self.data_type == "ADVERTISING":
                callback_data = f"sadver-{info['_id']}"
            elif self.data_type == 'FEEDBACK':
                author = await user_controller.get_one((User.id==info.author))
                callback_data = f"se_feed-{info.id}" if info.status == 'active' else f"do_feed-{info.id}"

            obj = InlineKeyboardButton(text=f'{i}', callback_data=callback_data)

            arr.append(obj)

            if len(arr) % limit == 0:
                keyboard.row(*arr)
                arr = []

            if self.data_type == 'ADVERTISING':
                text += f"<b>{i}.</b> {info.title}\n"
            if self.data_type == 'TEST':
                text += f"<b>{i}.</b> {info.question}\n"
            elif self.data_type == 'SECTION' or self.data_type == 'SUBJECT' or self.data_type == 'USER':
                text += f"<b>{i}.</b> {info.name}\n"
            elif self.data_type == 'FEEDBACK':
                text += f"<b>{i}.</b> {author.name} - {info.mark}\n"

        keyboard.row(*arr)

        inline_keyboard_buttons, extra_audio = [], []

        left_page_callback_data = f'left#{clause}#{page - 1}' if page != 1 else 'none'
        right_page_callback_data = f'right#{clause}#{page + 1}' if len(data) + offset != len(all_data) else 'none'

        if form == '':
            inline_keyboard_buttons = [
                InlineKeyboardButton(text='⬅', callback_data=left_page_callback_data),
                InlineKeyboardButton(text='❌', callback_data="delete"),
                InlineKeyboardButton(text='➡', callback_data=right_page_callback_data)
            ]
        elif form == 'TEST':
            inline_keyboard_buttons = [
                InlineKeyboardButton(text='⬅', callback_data=left_page_callback_data),
                InlineKeyboardButton(text='➡', callback_data=right_page_callback_data)
            ]

        keyboard.row(*inline_keyboard_buttons)

        if extra_audio:
            keyboard.row(*extra_audio)

        return dict(message=text, keyboard=keyboard, status=status)


def is_num(number) -> bool:
    try:
        int(number)
        return True
    except ValueError:
        return False


def date_info(day):
    year, month, date, hour, minutes = day.year, day.month, day.day, day.hour, day.minute

    return f"{year}-{month}-{date}. {hour}:{minutes}"


async def is_subscribed(bot: Bot, message: Message, CHANNEL_ID: int) -> bool:
    status = (await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.chat.id)).status

    if status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
        return False

    return True