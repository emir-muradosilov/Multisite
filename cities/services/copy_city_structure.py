from pages.models import ServicePage


def copy_city_structure(
    source_city,
    target_city
):
    """
    Копирует структуру услуг
    из Москвы в новый город.
    """

    parent_map = {}

    parents = ServicePage.objects.filter(
        city=source_city,
        parent__isnull=True
    )

    for page in parents:

        new_page = ServicePage.objects.create(
            city=target_city,
            parent=None,

            title=page.title,
            slug=page.slug,

            content=page.content,

            seo_title=page.seo_title,
            seo_description=page.seo_description,
            seo_keywords=page.seo_keywords,

            is_published=page.is_published,
            show_in_menu=page.show_in_menu,
            no_index=page.no_index,

            sort_order=page.sort_order,
            h1_title=page.h1_title,

            template=page.template,
        )

        parent_map[page.id] = new_page

        children = ServicePage.objects.filter(city=source_city, parent__isnull=False)

        for child in children:

            ServicePage.objects.create(
                city=target_city,

                parent=parent_map[
                    child.parent_id
                ],

                title=child.title,
                slug=child.slug,

                content=child.content,

                seo_title=child.seo_title,
                seo_description=child.seo_description,
                seo_keywords=child.seo_keywords,

                is_published=child.is_published,
                show_in_menu=child.show_in_menu,
                no_index=child.no_index,

                sort_order=child.sort_order,
                h1_title=child.h1_title,

                template=child.template,
            )

