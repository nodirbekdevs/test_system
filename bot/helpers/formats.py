from datetime import datetime
from bot.models.user import User
from bot.keyboards.keyboard_buttons import option


def introduction_format(name):
    message = (
        f"Bo'timizga xush kelibsiz {name}. <b>Tilni tanlang</b> {option['language']['uz']} \n"
        f"Добро пожаловать {name}. <b>Выберите язык</b> {option['language']['ru']}"
    )

    return message


def subject_format(data, language, is_editing=False):
    message, type = "", ""

    if language == option['language']['uz']:
        message += "Fan ma'lumotlari: \n"
        message += f"Тomi - {data['name']}\n"
        message += f"Tavsifi - {data['description']}\n"
    elif language == option['language']['ru']:
        message += "Информация о предмете: \n"
        message += f"Название - {data['name_ru']}\n"
        message += f"Описание - {data['description']}\n"

    if is_editing:
        message += f"\n\nNimani o'zgartirmoqchisiz ?" \
            if language == option['language']['uz'] else \
            f"\n\nЧто вы хотите изменить ?"
    else:
        if language == option['language']['uz']:
            message += f"Holati - {data['status']}\n"
            message += f"Qo'shilgan vaqti - {data['created_at'].strftime('%d.%m.%Y %H:%M')}"
        elif language == option['language']['ru']:
            message += f"Статус - {data['status']}\n"
            message += f"Добавлено время - {data['created_at'].strftime('%d.%m.%Y %H:%M')}"

    return message


def user_format(data, language, is_editing=False):
    message, type = "", ""

    if data.type == User.TypeChoices.ADMIN:
        type = 'Admin' if language == option['language']['uz'] else 'Админ'
    elif data.type == User.TypeChoices.INSTRUCTOR:
        type = option['types']['uz']['instructor'] \
            if language == option['language']['uz'] else \
            option['types']['uz']['instructor']
    elif data.type == User.TypeChoices.STUDENT:
        type = option['types']['uz']['student'] \
            if language == option['language']['uz'] else \
            option['types']['uz']['student']

    if language == option['language']['uz']:
        message += "Ma'lumotlaringiz: \n"
        message += f"Ism - {data.name}.\n"
        message += f"Telefon raqam - {data.number}.\n"
        message += f"Username - {data.username}.\n"
        message += f"Tanlangan til - {data.lang}.\n"
        message += f"Tur - {type}."
    elif language == option['language']['ru']:
        message += f"Ваша информация: \n"
        message += f"Имя - {data.name}.\n"
        message += f"Номер телефона - +{data.number}.\n"
        message += f"Username - {data.username}.\n"
        message += f"Выбранный язык - {data.lang}.\n"
        message += f"Тип - {type}."

    if is_editing:
        message += f"\n\nNimani o'zgartirmoqchisiz ?" \
            if language == option['language']['uz'] else \
            f"\n\nЧто вы хотите изменить ?"

    return message


def feedback_all_format(data, language=option['language']['uz']):
    message = tuple()

    if language == option['language']['uz']:
        message = (
            f"Umumiy izohlar soni - {data['count']}\n"
            f"Qabul qilingan izohlar soni - {data['active']}\n"
            f"\nKo'rilgan izohlar soni - {data['seen']}\n"
            f"Amalga oshirilgan izohlar soni - {data['done']}"
        )
    elif language == option['language']['ru']:
        message = (
            f"Общее количество комментариев - {data['count']}\n"
            f"Количество полученных комментариев - {data['active']}\n"
            f"\nКоличество просмотренных комментариев - {data['seen']}\n"
            f"Количество сделанных комментариев - {data['done']}"
        )

    return message


# def one_section_format(data, language):
#     message = tuple()
#
#     if language == option['language']['uz']:
#         message += (
#             f"Egasi - {data['user']}\n"
#             f"Fan - {data['subject']}\n"
#             f"Nomi - {data['name']}\n"
#             f"Tavsifi - {data['description']}\n"
#             f"Umumiy testlar - {data['total_tests']}\n"
#             f"Holat - {data['status']}\n"
#             f"Qo'shilgan vaqti - {data['created_at'].strftime('%d.%m.%Y %H:%M')}\n"
#         )
#     if language == option['language']['ru']:
#         message += (
#             f"Владелец - {data['user']}\n"
#             f"Наука - {data['subject']}\n"
#             f"Название - {data['name']}\n"
#             f"Описание - {data['description']}\n"
#             f"Общие тесты - {data['total_tests']}\n"
#             f"Статус - {data['status']}\n"
#             f"Добавлено время - {data['created_at'].strftime('%d.%m.%Y %H:%M')}\n"
#         )
#
#     return message


def one_section_format(data, language, is_editing=False):
    message = ""

    if not is_editing:
        message += f"Egasi - {data['user']}\n" if language == option['language'][
            'uz'] else f"Владелец - {data['user']}\n"

    if language == option['language']['uz']:
        message += f"Fan - {data['subject']}\n"
        message += f"Nomi - {data['name']}\n"
        message += f"Tavsifi - {data['description']}\n"
    if language == option['language']['ru']:
        message += f"Предмет - {data['subject']}\n"
        message += f"Название - {data['name']}\n"
        message += f"Описание - {data['description']}\n"

    if not is_editing:
        if language == option['language']['uz']:
            message += f"Testlar soni - {data['total_tests']}\n"
            message += f"Holat - {data['status']}\n"
            message += f"Qo'shilgan vaqti - {data['created_at'].strftime('%d.%m.%Y %H:%M')}\n"
        if language == option['language']['ru']:
            message += f"Количество тестов - {data['total_tests']}\n"
            message += f"Статус - {data['status']}\n"
            message += f"Добавлено время - {data['created_at'].strftime('%d.%m.%Y %H:%M')}\n"

    if is_editing:
        message += "\nTugaganini tasdiqlaysizmi ?" if language == option['language'][
            'uz'] else "\nПодтвердить завершение ?"

    return message


def feedback_format(data, language=option['language']['uz']):
    message = ""

    if language == option['language']['uz']:
        message += f"Avtor - {data['author']}\n"
        message += f"Bahosi - {data['mark']}\n"
        message += f"Sababi - {data['reason']}\n"
        message += f"Holati - {data['status']}\n"
        message += f"Yozilgan vaqti - {datetime.strptime(data['created_at'], '%d.%m.%Y %H:%M')}"
    if language == option['language']['ru']:
        message += f"Автор - {data['author']}\n"
        message += f"Рейтинг - {data['mark']}\n"
        message += f"Причина - {data['reason']}\n"
        message += f"Статус - {data['status']}\n"
        message += f"Записанное время - {datetime.strptime(data['created_at'], '%d.%m.%Y %H:%M')}"

    return message


def feedback_seen_format(data, language=option['language']['uz']):
    message = ""

    if language == option['language']['uz']:
        message += f"Assalomu Aleykum {data['name']}\n"
        message += f"Siz yozgan izoh ustida ishlar boshlandi\n"
        message += f"Izoh - {data['feedback']}"
    if language == option['language']['ru']:
        message += f"Assalomu Aleykum {data['name']}\n"
        message += f"Ваш комментарий обработан\n"
        message += f"Комментария - {data['feedback']}"

    return message


def feedback_done_format(data, language=option['language']['uz']):
    message = ""

    if language == option['language']['uz']:
        message += f"Assalomu Aleykum {data['name']}\n"
        message += f"Siz yozgan izoh ustida ishlar tugallandi. Muammo bartaraf etildi\n"
        message += f"Izoh - {data['feedback']}"
    elif language == option['language']['ru']:
        message += f"Assalomu Aleykum {data['name']}\n"
        message += f"Ваш комментарий обработан. Проблема решена\n"
        message += f"Комментария - {data['feedback']}"

    return message


def advertising_format(data, language, is_ending=False):
    message = ""

    message += f"<b>{data.title}</b>\n"
    message += f"\n<pre>{data.description}</pre>\n"

    if is_ending:
        message += "\nTugatilganini tasdiqlaysizmi ?" if language == option['language'][
            'uz'] else "\nПодтвердить завершение ?"

    return message


def advertising_number_format(data, language):
    message = tuple()

    if language == option['language']['uz']:
        message = (
            f"Umumiy reklamalar soni - {data['number']}\n"
            f"Tugallangan reklamalar soni - {data['active']}\n"
            f"O'chirilgan reklamalar soni - {data['inactive']}\n"
        )
    elif language == option['language']['ru']:
        message = (
            f"Общее количество объявлений - {data['number']}\n"
            f"Количество завершенных объявлений - {data['active']}\n"
            f"Количество удаленных объявлений - {data['inactive']}\n"
        )

    return message
#
#
# def salutation_format(data, is_editing=False):
#     message = ""
#
#     message += f"<b>{data['title']}</b>\n"
#     message += f"\n<pre>{data['content']}</pre>\n\n"
#
#     if is_editing:
#         message += "Tugaganini tasdiqlaysizmi ?"
#
#     return message
#
#
# def music_format(data, editing=""):
#     message = ""
#
#     message += f"<b>{data['name']}</b>\n"
#     message += f"\n<pre>{data['content']}</pre>\n\n"
#
#     if editing != "":
#         message += "Tugaganini tasdiqlaysizmi?"
#
#     return message
#
#
# def rear_format(name, editing=""):
#     message = ""
#
#     message += f"<b>{name}</b>\n\n"
#
#     if editing != "":
#         message += "Tugaganini tasdiqlaysizmi?"
#
#     return message
#
#
# def renown_format(name, editing=False):
#     message = ""
#
#     message += f"<b>{name}</b>\n\n"
#
#     if editing:
#         message += "Tugaganini tasdiqlaysizmi?"
#
#     return message
#
#
# def audio_making_format(data, language):
#     message = ""
#
#     if language == option['language']['uz']:
#         message += "Ma'lumotlar</b>\n"
#         message += f"Tabriklanuvchi odam -</b> {data['renown']}.\n"
#         message += f"Tabriklovchi odam -</b> {data['son_name']}.\n"
#         message += f"Tabrik -</b> {data['salutation']}.\n"
#         message += f"Musiqa -</b> {data['music']}.\n\n"
#         message += f"Tugaganini tasdiqlaysizmi ?</b>"
#     if language == option['language']['ru']:
#         message += f"Данные о аудио \n"
#         message += f"Поздравляющий человек - {data['renown']}.\n"
#         message += f"Поздравляющий человек - {data['son_name']}.\n"
#         message += f"Поздравления - {data['salutation']}.\n"
#         message += f"Музыка - {data['music']}.\n\n"
#         message += f"Вы можете подтвердить, что это сделано ?"
#
#     return message
#
#
# def audio_format(data, language):
#     message = ""
#
#     if language == option['language']['uz']:
#         message += "Ma'lumotlar \n"
#         message += f"Tabriklanuvchi odam - {data['renown']}.\n"
#         message += f"Tabriklovchi odam - {data['son_name']}.\n"
#         message += f"Tabrik - {data['salutation']}.\n"
#         message += f"Musiqa - {data['music']}.\n"
#     if language == option['language']['ru']:
#         message += "Данные о аудио \n"
#         message += f"Поздравляющий человек - {data['renown']}.\n"
#         message += f"Поздравляющий человек - {data['son_name']}.\n"
#         message += f"Поздравления - {data['salutation']}.\n"
#         message += f"Музыка - {data['music']}.\n"
#
#     return message
#
#
# def audio_caption_format(name, gender_type):
#     congratulated_name = f"❤{name} OPA❤" if gender_type == 'FEMALE' else f"❤{name} AKA❤"
#
#     text = f"""
#         {congratulated_name}
#         TAVALLUD AYYOMINGIZ MUBORAK BOLSIN👏👏👏👏
#         🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺
#         Murojaat uchun: +998990891789
#         Gruppamizga azo boling. Ushbu linkni bosing va gruppamizga azo bolasiz👇
#         https://t.me/Asomiddintabriknoma
#     """
#
#     return text
