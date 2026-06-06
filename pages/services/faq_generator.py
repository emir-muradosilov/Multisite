FAQ_PATTERNS = [

    "Сколько стоит {service} в {city}?",
    "Как заказать {service} в {city}?",
    "Сколько времени занимает {service}?",
    "Можно ли выполнять {service} в жилом доме?",
    "Какая техника используется для услуги {service}?",
    "Работаете ли вы ночью в {city}?",
    "Можно ли выполнять работы без пыли?",
    "Какие диаметры доступны для бурения?",
    "Нужны ли документы для проведения работ?",
    "Как быстро возможен выезд по {city}?",
]


def generate_faqs(page, city):

    faqs = []

    for question in FAQ_PATTERNS:

        faqs.append({
            'question': question.format(
                service=page.title.lower(),
                city=city.name
            )
        })

    return faqs