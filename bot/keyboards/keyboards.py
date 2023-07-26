from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot.helpers.config import IS_SUBSCRIBED
from bot.keyboards.keyboard_buttons import admin, instructor, student, option


"----- Start of admin keyboards -----"


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


def admin_settings_keyboard(language):
    uz_buttons = [
        [KeyboardButton(admin['settings']['uz']['name']), KeyboardButton(admin['settings']['uz']['number'])],
        [KeyboardButton(admin['settings']['uz']['lang'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(admin['settings']['ru']['name']), KeyboardButton(admin['settings']['ru']['number'])],
        [KeyboardButton(admin['settings']['ru']['lang'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    buttons = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def admin_admins_keyboard(language):
    uz_buttons = [
        [KeyboardButton(admin['admins']['uz']['all']), KeyboardButton(admin['admins']['uz']['add'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(admin['admins']['ru']['all']), KeyboardButton(admin['admins']['ru']['add'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    buttons = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


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


def one_seen_feedback_keyboard(feedback_id, feedback_mark, language):
    clause, info = "", ""

    back = option['back']['uz'] if language == option['language']['uz'] else option['back']['ru']

    if feedback_mark == option['feedback']['uz']['good'] or feedback_mark == option['feedback']['ru']['good']:
        clause = "Ko'rildi" if language == option['language']['uz'] else "Видено"
        info = 's_d'
    elif feedback_mark == option['feedback']['uz']['bad'] or feedback_mark == option['feedback']['ru']['bad']:
        clause = "Muommoni ko'rish boshlandi" if language == option['language']['uz'] else "Видение проблемы началось"
        info = 'seen'

    buttons = [
        [InlineKeyboardButton(text=clause, callback_data=f'{info}.{feedback_id}')],
        [InlineKeyboardButton(text=back, callback_data='back')]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def one_done_feedback_keyboard(feedback_id, language):
    clause, back, info = "", "", "done"

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


def admin_instructors_keyboard(language):
    uz_buttons = [
        [KeyboardButton(admin['instructors']['uz']['all']), KeyboardButton(admin['instructors']['uz']['add'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(admin['instructors']['ru']['all']), KeyboardButton(admin['instructors']['ru']['add'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    buttons = uz_buttons if language == option['languages']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def admin_students_keyboard(language):
    uz_buttons = [
        [KeyboardButton(admin['students']['uz']['all']), KeyboardButton(admin['students']['uz']['add'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(admin['students']['ru']['all']), KeyboardButton(admin['students']['ru']['add'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    buttons = uz_buttons if language == option['languages']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def admin_subjects_keyboard(language):
    uz_buttons = [
        [KeyboardButton(admin['subjects']['uz']['all']), KeyboardButton(admin['subjects']['uz']['add'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(admin['subjects']['ru']['all']), KeyboardButton(admin['subjects']['ru']['add'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    buttons = uz_buttons if language == option['languages']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def one_admin_keyboard(id) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete.admin.{id}")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


"----- End of admin keyboards -----"


"----- Start of option keyboards -----"


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


"----- End of option keyboards -----"


"----- Start of instructor keyboards -----"


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


def instructor_settings_keyboard(language):
    buttons_uz = [
        [KeyboardButton(instructor['settings']['uz']['name']), KeyboardButton(instructor['settings']['uz']['number'])],
        [KeyboardButton(instructor['settings']['uz']['lang'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    buttons_ru = [
        [KeyboardButton(instructor['settings']['ru']['name']), KeyboardButton(instructor['settings']['ru']['number'])],
        [KeyboardButton(instructor['settings']['ru']['lang'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    keyboard = buttons_uz if language == option['language']['uz'] else buttons_ru

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


def instructor_sections_keyboard(language):
    uz_buttons = [
        [KeyboardButton(instructor['sections']['uz']['all']), KeyboardButton(instructor['sections']['uz']['add'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(instructor['sections']['ru']['all']), KeyboardButton(instructor['sections']['ru']['add'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    buttons = uz_buttons if language == option['languages']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def one_section_keyboard(section_id, language):
    word, back = "", ""

    if language == option['language']['uz']:
        word = "O'chirish"
        back = option['back']['uz']
    elif language == option['language']['ru']:
        word = "Удалить"
        back = option['back']['ru']

    buttons = [
        [InlineKeyboardButton(text=word, callback_data=f"delete.section.{section_id}")],
        [InlineKeyboardButton(text=back, callback_data="back")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def instructor_tests_keyboard(language):
    uz_buttons = [
        [KeyboardButton(instructor['tests']['uz']['all']), KeyboardButton(instructor['tests']['uz']['add'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(instructor['tests']['ru']['all']), KeyboardButton(instructor['tests']['ru']['add'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    buttons = uz_buttons if language == option['languages']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def instructor_feedback_keyboard(language):
    uz_buttons = [
        [KeyboardButton(instructor['feedback']['uz']['add']), KeyboardButton(instructor['feedback']['uz']['my_feedback'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(instructor['feedback']['ru']['add']), KeyboardButton(instructor['feedback']['ru']['my_feedback'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    keyboard = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


"----- End of instructor keyboards -----"


"----- Start of student keyboards -----"


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


def student_settings_keyboard(language):
    uz_buttons = [
        [KeyboardButton(student['settings']['uz']['name']), KeyboardButton(student['settings']['uz']['number'])],
        [KeyboardButton(student['settings']['uz']['lang'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(instructor['student']['ru']['name']), KeyboardButton(student['settings']['ru']['number'])],
        [KeyboardButton(instructor['student']['ru']['lang'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    keyboard = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


def student_feedback_keyboard(language):
    uz_buttons = [
        [KeyboardButton(student['feedback']['uz']['add']), KeyboardButton(student['feedback']['uz']['my_feedback'])],
        [KeyboardButton(option['main']['uz'])]
    ]

    ru_buttons = [
        [KeyboardButton(student['feedback']['ru']['add']), KeyboardButton(student['feedback']['ru']['my_feedback'])],
        [KeyboardButton(option['main']['ru'])]
    ]

    keyboard = uz_buttons if language == option['language']['uz'] else ru_buttons

    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)


"----- End of student keyboards -----"


def subjects_keyboard(data, language, limit=3):
    buttons, arr = [], []

    for subject in data:
        if language == option['language']['uz']:
            arr.append(subject.name_uz)
        elif language == option['language']['ru']:
            arr.append(subject.name_ru)

        if len(arr) % limit == 0:
            buttons.append(arr)
            arr = []

    buttons.append(arr)

    buttons.append([option['back']['uz']]) if language == option['language']['uz'] else buttons.append([option['back']['ru']])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

