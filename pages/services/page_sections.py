import random


def build_page_sections(page):

    sections = [
        'cases',
        'reviews',
        'faq',
        'seo_text',
        'related',
        'portfolio_cases',
        'related_services',
        'popular_faq',
    ]

    # Для parent страниц
    if page.parent is None:
        sections.append('children')
    # Стабильный random
    random.seed(page.id)
    random.shuffle(sections)

    return sections


def get_random_cta(page):

    variants = [
        'cta_default',
        'cta_fast',
        'cta_discount',
    ]

    random.seed(page.id)

    return random.choice(variants)