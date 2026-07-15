from pages.models import ServicePage

from .clone import clone_model
from .utils import get_service_key



def copy_service_pages(
    source_city,
    target_city,
    replacer,
):
    """
    Копирование дерева услуг.

    Копирует:

    ServicePage
        |
        |-- parent
        |
        |-- children


    Возвращает:

    {
        old_page_id: new_page
    }

    Это нужно для восстановления связей
    FAQ, SEOBlock, PortfolioCase.
    """

    page_map = {}


    # -------------------------------------------------
    # 1. Родительские страницы
    # -------------------------------------------------

    parents = ServicePage.objects.filter(
        city=source_city,
        parent__isnull=True,
    ).order_by(
        "sort_order"
    )


    for page in parents:


        new_page = clone_model(
            page,
            replacer=replacer,
            city=target_city,
            parent=None,
        )


        page_map[page.id] = new_page



    # -------------------------------------------------
    # 2. Дочерние страницы
    # -------------------------------------------------

    children = ServicePage.objects.filter(
        city=source_city,
        parent__isnull=False,
    ).order_by(
        "sort_order"
    )


    for page in children:


        new_parent = page_map.get(
            page.parent_id
        )


        # защита от битой структуры

        if not new_parent:
            continue



        new_page = clone_model(
            page,
            replacer=replacer,
            city=target_city,
            parent=new_parent,
        )


        page_map[page.id] = new_page



    return page_map