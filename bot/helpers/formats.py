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
        message += f"Nomi - {data['name']}\n"
        message += f"Tavsifi - {data['description']}"
    elif language == option['language']['ru']:
        message += "Информация о предмете: \n"
        message += f"Название - {data['name']}\n"
        message += f"Описание - {data['description']}"

    if is_editing:
        message += f"\n\nTugaganini tasdiqlaysizmi ?" \
            if language == option['language']['uz'] else \
            f"\n\nМожете ли вы подтвердить, что это сделано ?"
    else:
        if language == option['language']['uz']:
            message += f"\nHolati - {data['status']}\n"
            message += f"Qo'shilgan vaqti - {data['created_at'].strftime('%d.%m.%Y %H:%M')}"
        elif language == option['language']['ru']:
            message += f"\nСтатус - {data['status']}\n"
            message += f"Добавлено время - {data['created_at'].strftime('%d.%m.%Y %H:%M')}"

    return message


def test_format(data, language, is_editing=False):
    message = ""

    if language == option['language']['uz']:
        message += "Test ma'lumotlari: \n"
        message += f"Egasi - {data['owner']}\n"
        message += f"Fan - {data['subject']}\n"
        message += f"Bo'lim - {data['section']}\n"
        message += f"Savol - {data['question']}\n"

        message += f"\nVariantlar\n"
        for index, variant in enumerate(data['variants'], start=1):
            message += f"{index}. {variant}\n"

        message += f"To'g'ri javob - {data['correct_answer']}"
    elif language == option['language']['ru']:
        message += "Информация о тесте: \n"
        message += f"Владелец - {data['owner']}\n"
        message += f"Предмет - {data['subject']}"
        message += f"Секция - {data['section']}"
        message += f"Вопрос - {data['question']}"

        message += f"\nВарианты\n"
        for index, variant in enumerate(data['variants'], start=1):
            message += f"{index}. {variant}\n"

        message += f"Правильный ответ - {data['correct_answer']}"

    if is_editing:
        message += f"\n\nTugaganini tasdiqlaysizmi ?" \
            if language == option['language']['uz'] else \
            f"\n\nМожете ли вы подтвердить, что это сделано ?"
    else:
        if language == option['language']['uz']:
            message += f"\nHolati - {data['status']}\n"
            message += f"Qo'shilgan vaqti - {data['created_at'].strftime('%d.%m.%Y %H:%M')}"
        elif language == option['language']['ru']:
            message += f"\nСтатус - {data['status']}\n"
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


def section_format(data, language, is_editing=False):
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

    message += f"<b>{data['title']}</b>\n"
    message += f"\n<pre>{data['description']}</pre>\n"

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