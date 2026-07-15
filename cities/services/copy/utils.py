from pages.models import ServicePage


def get_service_key(page: ServicePage):
    """
    Возвращает уникальный ключ страницы.

    Используется для восстановления
    связей после клонирования.

    Родитель:
        almaznoe-burenie

    Дочерняя:
        almaznoe-burenie/burenie-v-potolok
    """

    if page.parent_id:

        return (
            page.parent.slug,
            page.slug,
        )

    return (
        None,
        page.slug,
    )


def build_page_map(service_pages):
    """
    Строит словарь:

        (parent_slug, slug) -> ServicePage
    """

    result = {}

    for page in service_pages:

        result[get_service_key(page)] = page

    return result