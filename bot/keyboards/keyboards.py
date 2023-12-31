from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot.helpers.config import IS_SUBSCRIBED, ADMIN, SECTION, TEST, INSTRUCTOR, SUBJECT, STUDENT, SEEN, DONE
from bot.keyboards.keyboard_buttons import admin, instructor, student, option, all
# from bot.helpers.utils import generate_variants


def generate_variants(item_count):
    base = ord('a')
    return [chr(base + i) for i in range(len(item_count))]


def language_definer(language):
    return 'uz' if language == option['language']['uz'] else 'ru'


def all_users_keyboard(users, language, limit=3):
    buttons, arr = [], []

    for user in users:
        arr.append(KeyboardButton(user.name))

        if len(arr) % limit == 0:
            buttons.append(arr)
            arr = []

    buttons.append(arr)

    buttons.append([option['back'][language_definer(language)]])

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def admin_pages_keyboard(language):
    lang = language_definer(language)

    buttons = [
        [KeyboardButton(admin['pages'][lang]['settings']), KeyboardButton(admin['pages'][lang]['admins'])],
        [KeyboardButton(admin['pages'][lang]['instructors']), KeyboardButton(admin['pages'][lang]['students'])],
        [KeyboardButton(admin['pages'][lang]['subjects']), KeyboardButton(admin['pages'][lang]['advertisements'])],
        [KeyboardButton(admin['pages'][lang]['feedback'])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def admin_keyboard(section_type, language):
    section = ''

    lang = language_definer(language)

    if section_type == ADMIN:
        section = 'admins'
    elif section_type == INSTRUCTOR:
        section = 'instructors'
    elif section_type == SUBJECT:
        section = 'subjects'
    elif section_type == STUDENT:
        section = 'students'

    buttons = [
        [KeyboardButton(admin[section][lang]['all']), KeyboardButton(admin[section][lang]['add'])],
        [KeyboardButton(option['main'][lang])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def one_admin_keyboard(user_id, language, data_type: str = ADMIN):
    clause, back, kw = '', '', ''

    if data_type == ADMIN:
        kw = 'admin'
    elif data_type == INSTRUCTOR:
        kw = 'instructor'
    elif data_type == STUDENT:
        kw = 'student'
    elif data_type == SUBJECT:
        kw = 'subject'

    if language == option['language']['uz']:
        clause = "O'chirish"
        back = option['back']['uz']
    if language == option['language']['ru']:
        clause = "Удалить"
        back = option['back']['ru']

    buttons = [
        [InlineKeyboardButton(text=clause, callback_data=f"delete.{kw}.{user_id}")],
        [InlineKeyboardButton(text=back, callback_data="back")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_feedback_keyboard(language):
    lang = language_definer(language)

    buttons = [
        [KeyboardButton(admin['feedback'][lang]['number'])],
        [KeyboardButton(admin['feedback'][lang]['read']), KeyboardButton(admin['feedback'][lang]['doing'])],
        [KeyboardButton(option['main'][lang])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def one_feedback_keyboard(feedback_id, feedback_type, language, feedback_mark = ''):
    clause, info = "", ""

    back = option['back']['uz'] if language == option['language']['uz'] else option['back']['ru']

    if feedback_type == SEEN:
        if feedback_mark == option['feedback']['uz']['good'] or feedback_mark == option['feedback']['ru']['good']:
            clause = "Ko'rildi" if language == option['language']['uz'] else "Видено"
            info = 's_d'
        elif feedback_mark == option['feedback']['uz']['bad'] or feedback_mark == option['feedback']['ru']['bad']:
            clause = "Muommoni ko'rish boshlandi" if language == option['language']['uz'] else "Видение проблемы началось"
            info = 'seen'
    elif feedback_type == DONE:
        if language == option['language']['uz']:
            clause = "Muommoni hal qilindi"
            back = option['back']['uz']
        if language == option['language']['ru']:
            clause = "Задача решена"
            back = option['back']['ru']

    buttons = [
        [InlineKeyboardButton(text=clause, callback_data=f'{info}.{feedback_id}')],
        [InlineKeyboardButton(text=back, callback_data='back')]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_advertisements_keyboard(language):
    lang = language_definer(language)

    buttons = [
        [KeyboardButton(admin['advertisements'][lang]['number'])],
        [KeyboardButton(admin['advertisements'][lang]['all']), KeyboardButton(admin['advertisements'][lang]['add'])],
        [KeyboardButton(option['main'][lang])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def one_advertising_keyboard(id, language):
    lang = language_definer(language)

    send_ad, delete_ad, back = option['send_advertise'][lang], option['delete_advertise'][lang], option['back'][lang]

    buttons = [
        [InlineKeyboardButton(text=send_ad, callback_data=f'send_ad.{id}')],
        [InlineKeyboardButton(text=delete_ad, callback_data=f'delete_ad.{id}')],
        [InlineKeyboardButton(text=back, callback_data=f'back')]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def settings_keyboard(language):
    lang = language_definer(language)

    buttons = [
        [KeyboardButton(all['settings'][lang]['name']), KeyboardButton(all['settings'][lang]['number'])],
        [KeyboardButton(all['settings'][lang]['lang'])],
        [KeyboardButton(option['main'][lang])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def instructor_pages_keyboard(language):
    lang = language_definer(language)

    buttons = [
        [KeyboardButton(instructor['pages'][lang]['settings']), KeyboardButton(instructor['pages'][lang]['feedback'])],
        [KeyboardButton(instructor['pages'][lang]['sections']), KeyboardButton(instructor['pages'][lang]['tests'])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def instructor_keyboard(section_type, language):
    section = ''

    lang = language_definer(language)

    if section_type == SECTION:
        section = 'sections'
    elif section_type == TEST:
        section = 'tests'

    buttons = [
        [KeyboardButton(instructor[section][lang]['all']), KeyboardButton(instructor[section][lang]['add'])],
        [KeyboardButton(option['main'][lang])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def one_instructor_keyboard(section_id, data_type, language):
    kw, word, back = "", "", ""

    if data_type == SECTION:
        kw = 'section'
    if data_type == TEST:
        kw = 'test'

    if language == option['language']['uz']:
        word = "O'chirish"
        back = option['back']['uz']
    elif language == option['language']['ru']:
        word = "Удалить"
        back = option['back']['ru']

    buttons = [
        [InlineKeyboardButton(text=word, callback_data=f"delete.{kw}.{section_id}")],
        [InlineKeyboardButton(text=back, callback_data="back")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def student_pages_keyboard(language):
    lang = language_definer(language)

    buttons = [
        [KeyboardButton(instructor['pages'][lang]['settings']), KeyboardButton(instructor['pages'][lang]['feedback'])],
        [KeyboardButton(instructor['pages'][lang]['tests'])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def student_instructor_feedback_keyboard(language):
    lang = language_definer(language)

    buttons = [
        [KeyboardButton(all['feedback'][lang]['add']), KeyboardButton(all['feedback'][lang]['my_feedback'])],
        [KeyboardButton(option['main'][lang])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def subjects_sections_keyboard(datas, language, limit=3):
    buttons, arr = [], []

    for data in datas:
        if language == option['language']['uz']:
            arr.append(KeyboardButton(data.name_uz))
        elif language == option['language']['ru']:
            arr.append(KeyboardButton(data.name_ru))

        if len(arr) % limit == 0:
            buttons.append(arr)
            arr = []

    buttons.append(arr)

    buttons.append([option['back'][language_definer(language)]])

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def is_subscribed_keyboard(language_code, CHANNEL_LINK) -> InlineKeyboardMarkup:
    uz_buttons = [
        [InlineKeyboardButton('Obunani tekshiring', callback_data=f'{IS_SUBSCRIBED}')],
        [InlineKeyboardButton("Kanalga obuna bo'ling", url=f'{CHANNEL_LINK}')],
    ]

    ru_buttons = [
        [InlineKeyboardButton('Проверить подписку', callback_data=f'{IS_SUBSCRIBED}')],
        [InlineKeyboardButton('Подписаться на канал', url=f'{CHANNEL_LINK}')],
    ]

    inline_keyboard = uz_buttons if language_code in ['uz', 'en'] else ru_buttons

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def feedback_keyboard(language):
    lang = language_definer(language)

    buttons = [
        [KeyboardButton(option['feedback'][lang]['good']), KeyboardButton(option['feedback'][lang]['bad'])],
        [KeyboardButton(option['back'][lang])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def language_keyboard(is_editing=None, language=None):
    lang = language_definer(language)

    buttons = [[KeyboardButton(option['language']['uz']), KeyboardButton(option['language']['ru'])]]

    if is_editing:
        buttons.append([option['back'][lang]])

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def main_keyboard(language):
    lang = language_definer(language)

    buttons = [[KeyboardButton(option['main'][lang])]]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def start_keyboard():
    buttons = [[KeyboardButton(option['start'])]]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons, one_time_keyboard=True)


def confirmation_keyboard(language):
    lang = language_definer(language)

    buttons = [[KeyboardButton(option['confirmation'][lang]), KeyboardButton(option['not_to_confirmation'][lang])]]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def next_keyboard(language):
    lang = language_definer(language)

    buttons = [
        [KeyboardButton(option['next'][lang])],
        [KeyboardButton(option['back'][lang])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def back_keyboard(language):
    lang = language_definer(language)

    buttons = [[KeyboardButton(option['back'][lang])]]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def type_keyboard(language):
    lang = language_definer(language)

    buttons = [[KeyboardButton(option['types'][lang]['instructor']), KeyboardButton(option['types'][lang]['student'])]]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def confirmation_advertising_keyboard(language):
    lang = language_definer(language)

    buttons = [
        [KeyboardButton(option['confirmation_advertising'][lang]['yes']),
         KeyboardButton(option['confirmation_advertising'][lang]['no'])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def send_contact_keyboard(language):
    lang = language_definer(language)

    buttons = [[KeyboardButton(option['send'][lang], request_contact=True)]]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def confirmation_with_back_keyboard(language):
    lang = language_definer(language)

    buttons = [
        [KeyboardButton(option['confirmation'][lang]), KeyboardButton(option['not_to_confirmation'][lang])],
        [KeyboardButton(option['back'][lang])]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def start_test_keyboard(language):
    lang = language_definer(language)

    text = "Test ishlashni boshlash" if language == option['language']['uz'] else "Начать тестовый запуск"

    buttons = [
        [InlineKeyboardButton(text=text, callback_data='start_test')],
        [InlineKeyboardButton(text=option['back'][lang], callback_data='delete')]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def test_solution_keyboard(test, language, answer=False):
    lang, variants = language_definer(language), generate_variants(test['variants_uz'])

    buttons = []

    for test_variant, variant in zip(test[f'variants_{lang}'], variants):
        button_text = f'{variant.upper()}. {test_variant}'

        if answer and answer == test_variant:
            button_text = f'{variant.upper()}. {test_variant} ✅'

        buttons.append([InlineKeyboardButton(text=button_text, callback_data=f'solving_{test_variant}')])

    buttons.append([InlineKeyboardButton(text=option['finish'][lang], callback_data='finish_test')])

    buttons.append([
        InlineKeyboardButton(text='⬅', callback_data='prev_test'),
        InlineKeyboardButton(text='❌', callback_data="delete"),
        InlineKeyboardButton(text='➡', callback_data='next_test')
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
