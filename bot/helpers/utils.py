from aiogram import Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberStatus

from deep_translator import GoogleTranslator
from asyncio import get_event_loop, to_thread

from bot.controllers import (
    advertising_controller, section_controller, subject_controller, test_controller, user_controller,
    feedback_controller
)
from bot.models.user import User
from bot.models.feedback import StatusChoices as FeedbackStatusChoices
from bot.keyboards.keyboard_buttons import option
from bot.helpers.config import INSTRUCTOR, SUBJECT, TEST, ADMIN, SECTION, STUDENT
from bot.keyboards.keyboards import (
    admin_advertisements_keyboard,
    admin_keyboard,
    admin_feedback_keyboard,
    instructor_keyboard,
    student_instructor_feedback_keyboard
)



def translator(sentence_uz, sentence_ru, language):
    return sentence_uz if language == option['language']['uz'] else sentence_ru


class Pagination:
    def __init__(self, data_type: str):
        self.data_type = data_type

    async def paginate(self, page: int, limit: int, query: dict, language: str, order_by_columns=[],
                       form: str = '') -> dict:
        text, clause, data, all_data, keyboard, arr, author, status = "", "", [], [], InlineKeyboardMarkup(), [], {}, True

        offset = limit * (page - 1)

        if self.data_type == 'SUBJECT':
            data = await subject_controller.get_pagination(query, offset, limit)
            all_data = await subject_controller.get_all(query)
            clause = 'subjects'
        elif self.data_type == 'SECTION':
            data = await section_controller.get_pagination(query, offset, limit)
            all_data = await section_controller.get_all(query)
            clause = 'sections'
        elif self.data_type == 'ADVERTISING':
            data = await advertising_controller.get_pagination(query, offset, limit)
            all_data = await advertising_controller.get_all(query)
            clause = 'advertising'
        elif self.data_type in ['ADMIN', 'INSTRUCTOR', 'STUDENT']:
            data = await user_controller.get_pagination(query, offset, limit)
            all_data = await user_controller.get_all(query)
            if self.data_type == 'ADMIN':
                clause = 'admins'
            if self.data_type == 'INSTRUCTOR':
                clause = 'instructors'
        elif self.data_type == 'FEEDBACK':
            data = await feedback_controller.get_pagination(query, offset, limit)
            all_data = await feedback_controller.get_all(query)
            if query['status'] == 'active':
                clause = 'selfeedback'
            elif query['status'] == 'seen':
                clause = 'dofeedback'
        elif self.data_type == 'TEST':
            data = await test_controller.get_pagination(query, offset, limit, order_by_columns)
            all_data = await test_controller.get_all(query)
            clause = 'tests'
        elif self.data_type == 'USER':
            data = await user_controller.get_pagination(query, offset, limit)
            all_data = await user_controller.get_all(query)
            clause = 'users'

        if len(data) <= 0:
            if self.data_type == 'SUBJECT':
                text = translator("Hozircha fanlar qo'shilmagan", "Ни одна предмет еще не добавлена", language)
                keyboard = admin_keyboard(SUBJECT, language)
            elif self.data_type == 'SECTION':
                text = translator("Hozircha bo'limlar qo'shilmagan", "Секции еще не добавлены", language)
                keyboard = instructor_keyboard(SECTION, language)
            elif self.data_type == 'TEST':
                text = translator(
                    "Hozircha bu bo'lim uchun testlar qo'shilmagan",
                    "Тесты для этой секции пока не добавлены",
                    language
                )
                keyboard = instructor_keyboard(TEST, language)
            elif self.data_type == 'PLACE':
                text = "Hozircha bu tip uchun tabriklar qo'shilmagan" \
                    if language == option['language']['uz'] else \
                    "Поздравления для этого типа пока не добавлены"
            elif self.data_type == 'ADVERTISING':
                text = translator("Hozircha reklamalar qo'shilmagan", "Объявления еще не добавлены", language)
                keyboard = admin_advertisements_keyboard(language)
            elif self.data_type == 'FEEDBACK':
                if query['status'] == FeedbackStatusChoices.ACTIVE:
                    text = translator('Hali izohlar mavjud emas', 'Комментариев пока нет', language)
                elif query['status'] == FeedbackStatusChoices.SEEN:
                    text = translator('Hali bajarilayotgan izohlar mavjud emas', 'Комментариев пока нет', language)
                keyboard = student_instructor_feedback_keyboard(language) \
                    if 'author' in query else \
                    admin_feedback_keyboard(language)
            elif self.data_type in ['USER', 'ADMINS', 'INSTRUCTORS']:

                if query['type'] == User.TypeChoices.ADMIN:
                    text = translator("Hozircha adminlar topilmadi", "Админы пока не найдены", language)
                    keyboard = admin_keyboard(ADMIN, language)
                elif query['type'] == User.TypeChoices.INSTRUCTOR:
                    text = translator("Hozircha instruktorlar topilmadi", "Инструкторы пока не найдены", language)
                    keyboard = admin_keyboard(INSTRUCTOR, language)
                elif query['type'] == User.TypeChoices.STUDENT:
                    text = translator("Hozircha studentlar topilmadi", "Студенты пока не найдены", language)
                    keyboard = admin_keyboard(STUDENT, language)

            status = False

            return dict(message=text, keyboard=keyboard, status=status)

        text = translator(
            f'<b>Hozirgi: {offset + 1}-{len(data) + offset}, Jami: {len(all_data)}</b>\n\n',
            f'<b>Текущий: {offset + 1}-{len(data) + offset}, Общий: {len(all_data)}</b>\n\n',
            language
        )

        for i, info in enumerate(data, start=1):
            callback_data = ""

            if self.data_type == 'ADMIN':
                callback_data = f"sadmin-{info.id}"
            if self.data_type == 'INSTRUCTOR':
                callback_data = f"sins-{info.id}"
            elif self.data_type == 'SUBJECT':
                callback_data = f"ssubject-{info.id}"
            elif self.data_type == 'SECTION':
                callback_data = f"ssection-{info.id}"
            elif self.data_type == 'PLACE':
                callback_data = f"splace-{info.id}"
            elif self.data_type == 'TEST':
                callback_data = f"stest-{info.id}"
            elif self.data_type == 'USER':
                callback_data = f"suser-{info.id}"
            elif self.data_type == "ADVERTISING":
                callback_data = f"sadver-{info.id}"
            elif self.data_type == 'FEEDBACK':
                author = await user_controller.get_one(dict(id=info.user_id))
                callback_data = f"se_feed-{info.id}" if info.status == FeedbackStatusChoices.ACTIVE else f"do_feed-{info.id}"

            obj = InlineKeyboardButton(text=f'{i}', callback_data=callback_data)

            arr.append(obj)

            if len(arr) % limit == 0:
                keyboard.row(*arr)
                arr = []

            if self.data_type in ['ADMIN', 'INSTRUCTOR', 'STUDENT']:
                text += f"<b>{i}.</b>  {info.name} - {info.telegram_id}\n"
            if self.data_type == 'ADVERTISING':
                text += f"<b>{i}.</b> {info.title}\n"
            if self.data_type == 'TEST':
                text += f"<b>{i}.</b> {translator(info.question_uz, info.question_ru, language)}\n"
            elif self.data_type == 'SECTION':
                text += f"<b>{i}.</b> {translator(info.name_uz, info.name_ru, language)}\n"
            elif self.data_type == 'SUBJECT':
                text += f"<b>{i}.</b> {translator(info.name_uz, info.name_ru, language)}\n"
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


def language_definer(language):
    return 'uz' if language == option['language']['uz'] else 'ru'


async def translate_text(translator, text):
    translated_text = await to_thread(translator.translate, text)
    return translated_text.capitalize()