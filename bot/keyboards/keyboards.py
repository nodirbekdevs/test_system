from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot.helpers.config import IS_SUBSCRIBED, ADMIN, SECTION, TEST, INSTRUCTOR, SUBJECT, STUDENT, SEEN, DONE
from bot.keyboards.keyboard_buttons import admin, instructor, student, option, all


def admin_pages_keyboard(language):
    uz_buttons = [
        [KeyboardButton(admin['pages']['uz']['settings']), KeyboardButton(admin['pages']['uz']['admins'])],
        [KeyboardButton(admin['pages']['uz']['instructors']), KeyboardButton(admin['pages']['uz']['students'])],
        [KeyboardButton(admin['pages']['uz']['subjects']), KeyboardButton(admin['pages']['uz']['advertisements'])],
        [KeyboardButton(admin['pages']['uz']['feedback'])]
    ]

    ru_buttons = [
        [KeyboardButton(admin['pages']['ru']['settings']), KeyboardButton(admin['pages']['ru']['admins'])],
        [KeyboardButton(admin['pages']['ru']['instructors']), KeyboardButton(admin['pages']['ru']['students'])],
        [KeyboardButton(admin['pages']['ru']['subjects']), KeyboardButton(admin['pages']['ru']['advertisements'])],
        [KeyboardButton(admin['pages']['ru']['feedback'])]
    ]

    buttons = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def admin_keyboard(section_type, language):
    section = ''

    if section_type == ADMIN:
        section = 'admins'
    elif section_type == INSTRUCTOR:
        section = 'instructors'
    elif section_type == SUBJECT:
        section = 'subjects'
    elif section_type == STUDENT:
        section = 'students'

    buttons = [
        [KeyboardButton(admin[section][language]['all']), KeyboardButton(admin[section][language]['add'])],
        [KeyboardButton(option['main'][language])]
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
    uz_buttons = [
        [KeyboardButton(admin['feedback']['uz']['number'])],
        [KeyboardButton(admin['feedback']['uz']['read']), KeyboardButton(admin['feedback']['uz']['doing'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(admin['feedback']['uz']['number'])],
        [KeyboardButton(admin['feedback']['uz']['read']), KeyboardButton(admin['feedback']['uz']['doing'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    buttons = uz_buttons if language == option['language']['uz'] else ru_buttons

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
    uz_buttons = [
        [KeyboardButton(admin['advertisements']['uz']['number'])],
        [KeyboardButton(admin['advertisements']['uz']['all']), KeyboardButton(admin['advertisements']['uz']['add'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(admin['advertisements']['uz']['number'])],
        [KeyboardButton(admin['advertisements']['uz']['all']), KeyboardButton(admin['advertisements']['uz']['add'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    buttons = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def one_advertising_keyboard(id, language):
    send_ad, delete_ad, back = "", "", ""

    if language == option['language']['uz']:
        send_ad = option['send_advertise']['uz']
        delete_ad = option['delete_advertise']['uz']
        back = option['back']['uz']
    elif language == option['language']['ru']:
        send_ad = option['send_advertise']['ru']
        delete_ad = option['delete_advertise']['ru']
        back = option['back']['ru']

    buttons = [
        [InlineKeyboardButton(text=send_ad, callback_data=f'send_ad.{id}')],
        [InlineKeyboardButton(text=delete_ad, callback_data=f'delete_ad.{id}')],
        [InlineKeyboardButton(text=back, callback_data=f'back')]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def settings_keyboard(language):
    uz_buttons = [
        [KeyboardButton(all['settings']['uz']['name']), KeyboardButton(all['settings']['uz']['number'])],
        [KeyboardButton(all['settings']['uz']['lang'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(all['settings']['ru']['name']), KeyboardButton(all['settings']['ru']['number'])],
        [KeyboardButton(all['settings']['ru']['lang'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    buttons = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def instructor_pages_keyboard(language):
    uz_buttons = [
        [KeyboardButton(instructor['pages']['uz']['settings']), KeyboardButton(instructor['pages']['uz']['feedback'])],
        [KeyboardButton(instructor['pages']['uz']['sections']), KeyboardButton(instructor['pages']['uz']['tests'])]
    ]

    ru_buttons = [
        [KeyboardButton(instructor['pages']['ru']['settings']), KeyboardButton(instructor['pages']['ru']['feedback'])],
        [KeyboardButton(instructor['pages']['ru']['sections']), KeyboardButton(instructor['pages']['ru']['tests'])]
    ]

    keyboard = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


def instructor_keyboard(section_type, language):
    section = ''

    if section_type == SECTION:
        section = 'sections'
    elif section_type == TEST:
        section = 'tests'

    uz_buttons = [
        [KeyboardButton(instructor[section]['uz']['all']), KeyboardButton(instructor[section]['uz']['add'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(instructor[section]['ru']['all']), KeyboardButton(instructor[section]['ru']['add'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    buttons = uz_buttons if language == option['languages']['uz'] else ru_buttons

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
    uz_buttons = [
        [KeyboardButton(instructor['pages']['uz']['settings']), KeyboardButton(instructor['pages']['uz']['feedback'])],
        [KeyboardButton(instructor['pages']['uz']['tests'])]
    ]

    ru_buttons = [
        [KeyboardButton(instructor['pages']['ru']['settings']), KeyboardButton(instructor['pages']['ru']['feedback'])],
        [KeyboardButton(instructor['pages']['ru']['tests'])]
    ]

    keyboard = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


def student_instructor_feedback_keyboard(language):
    uz_buttons = [
        [KeyboardButton(all['feedback']['uz']['add']), KeyboardButton(all['feedback']['uz']['my_feedback'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(all['feedback']['ru']['add']), KeyboardButton(all['feedback']['ru']['my_feedback'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    keyboard = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


def subjects_sections_keyboard(datas, language, limit=3):
    buttons, arr = [], []

    for data in datas:
        if language == option['language']['uz']:
            arr.append(data.name_uz)
        elif language == option['language']['ru']:
            arr.append(data.name_ru)

        if len(arr) % limit == 0:
            buttons.append(arr)
            arr = []

    buttons.append(arr)

    buttons.append([option['back']['uz']]) if language == option['language']['uz'] else buttons.append([option['back']['ru']])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


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
    uz_buttons = [
        [KeyboardButton(option['feedback']['uz']['good']), KeyboardButton(option['feedback']['uz']['bad'])],
        [KeyboardButton(option['back']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(option['feedback']['ru']['good']), KeyboardButton(option['feedback']['ru']['bad'])],
        [KeyboardButton(option['back']['ru'])]
    ]

    keyboard = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


def language_keyboard(is_editing=None, language=None):
    buttons = [[KeyboardButton(option['language']['uz']), KeyboardButton(option['language']['ru'])]]

    if is_editing:
        buttons.append([option['back']['uz']]) \
            if language == option['language']['uz'] else \
            buttons.append([option['back']['ru']])

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def main_keyboard(language):
    uz_buttons = [[KeyboardButton(option['main']['uz'])]]

    ru_buttons = [[KeyboardButton(option['main']['ru'])]]

    keyboard = uz_buttons if language == 'UZ' else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


def start_keyboard():
    buttons = [[KeyboardButton(option['start'])]]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons, one_time_keyboard=True)


def confirmation_keyboard(language):
    uz_buttons = [[KeyboardButton(option['confirmation']['uz']), KeyboardButton(option['not_to_confirmation']['uz'])]]

    ru_buttons = [[KeyboardButton(option['confirmation']['ru']), KeyboardButton(option['not_to_confirmation']['ru'])]]

    keyboard = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


def next_keyboard(language):
    uz_buttons = [
        [KeyboardButton(option['next']['uz'])],
        [KeyboardButton(option['back']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(option['next']['ru'])],
        [KeyboardButton(option['back']['ru'])]
    ]

    keyboard = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


def back_keyboard(language):
    word = option['back']['uz'] if language == option['language']['uz'] else option['back']['ru']

    keyboard = [[KeyboardButton(word)]]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


def type_keyboard(language):
    uz_buttons = [
        [KeyboardButton(option['types']['uz']['instructor']), KeyboardButton(option['types']['uz']['student'])],
    ]

    ru_buttons = [
        [KeyboardButton(option['types']['ru']['instructor']), KeyboardButton(option['types']['ru']['student'])],
    ]

    buttons = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def confirmation_advertising_keyboard(language):
    uz_buttons = [
        [KeyboardButton(option['confirmation_advertising']['uz']['yes']),
         KeyboardButton(option['confirmation_advertising']['uz']['no'])]
    ]

    ru_buttons = [
        [KeyboardButton(option['confirmation_advertising']['ru']['yes']),
         KeyboardButton(option['confirmation_advertising']['ru']['no'])]
    ]

    buttons = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def send_contact_keyboard(language):
    send = option['send']['uz'] if language == option['language']['uz'] else option['send']['ru']

    buttons = [
        [KeyboardButton(send, request_contact=True)]
    ]

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def confirmation_with_back_keyboard(language):
    uz_buttons = [
        [KeyboardButton(option['confirmation']['uz']), KeyboardButton(option['not_to_confirmation']['uz'])],
        [KeyboardButton(option['back']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(option['confirmation']['ru']), KeyboardButton(option['not_to_confirmation']['ru'])],
        [KeyboardButton(option['back']['ru'])]
    ]

    keyboard = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)
